from __future__ import annotations

import asyncio
import json

import httpx
import pytest
from epoch_sdk.contracts import RunRequest
from epoch_sdk.research_operations import ResearchOperationsClient, ResearchRecord
from epoch_sdk.supervisor import SupervisorClient
from stratifyx.core.api_error import ApiError

REQUEST = {"task": "Explain", "outputs": [{"name": "answer", "type": "text", "instructions": "Explain"}]}
RECORD = {"request_id": "req_" + "a" * 32, "version": 0, "created_at_ms": 1, "updated_at_ms": 1, "phase": "accepted", "interaction": "one_shot", "request": REQUEST}


def test_platform_lifecycle_uses_its_own_origin_and_renewing_credential():
    async def scenario():
        calls = []
        issued = []
        async def token():
            issued.append(len(issued)); return 'renewed-' + str(len(issued))
        def handle(request):
            calls.append(request)
            assert request.url.host == 'platform.invalid'
            assert request.headers['Authorization'] == 'Bearer renewed-' + str(len(calls))
            return httpx.Response(200, json=RECORD)
        supervisor = SupervisorClient._connect(graph_url='https://graph.invalid', backend_url='https://native.invalid', platform_url='https://platform.invalid', token=token, transport=httpx.MockTransport(handle))
        try:
            row = await supervisor.research_operations.create_sdk_request(request=RunRequest.model_validate(REQUEST))
            assert row.interaction == 'one_shot'
            await supervisor.research_operations.get_sdk_request(row.request_id)
        finally:
            await supervisor.aclose()
        assert len(calls) == len(issued) == 2
        assert json.loads(calls[0].content) == {'request': REQUEST}
    asyncio.run(scenario())


def test_writes_are_once_only_and_failure_does_not_become_a_record():
    async def scenario():
        calls = []
        def handle(request):
            calls.append(request); return httpx.Response(503, json={'message': 'Unavailable'})
        client = ResearchOperationsClient('https://platform.invalid', 'owner', transport=httpx.MockTransport(handle))
        try:
            with pytest.raises(ApiError) as failure:
                await client.create_sdk_request(request=RunRequest.model_validate(REQUEST))
            assert failure.value.status_code == 503
        finally:
            await client.aclose()
        assert len(calls) == 1
    asyncio.run(scenario())


def test_closed_record_rejects_unreadable_accepted_input_and_missing_interaction():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ResearchRecord.model_validate_json(json.dumps({**RECORD, 'request': {**REQUEST, 'context': ['  ']}}))
    with pytest.raises(ValidationError):
        ResearchRecord.model_validate_json(json.dumps({key: value for key, value in RECORD.items() if key != 'interaction'}))


def test_one_shot_unrecognized_pause_persists_failure_instead_of_waiting():
    from test_research import clients, REQUEST as FIXTURE_REQUEST
    from epoch_sdk.research import ResearchError
    async def scenario():
        async with clients(interrupt=True) as (client, record, _, _):
            ordinary = client.research_operations.create_sdk_request
            async def create(**kwargs):
                result = await ordinary(**kwargs)
                record['interaction'] = 'one_shot'
                return result.model_copy(update={'interaction': 'one_shot'})
            client.research_operations.create_sdk_request = create
            with pytest.raises(ResearchError) as failure:
                await client.research(RunRequest.model_validate(FIXTURE_REQUEST))
            assert failure.value.error.code == 'EXECUTION_FAILED'
            assert record['phase'] == 'failed'
    asyncio.run(scenario())
