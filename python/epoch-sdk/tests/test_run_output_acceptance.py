"""Opt-in real Backend/EpochAI HTTP campaign with a controlled model provider.

Requires the explicit loopback engineering fixtures from Backend and EpochAI.
There is no mock HTTP transport or substitute execution result in this campaign.
"""
import asyncio
import json
import os
from pathlib import Path
import time
import uuid

import httpx
import pytest
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError
from stratifyx.types import (
    CreateExecutionOutputEdit, CreateSdkExecutionRequest, DashboardEditAction, DashboardEditAddress,
    DashboardEditComponentKind, DashboardEditField, DashboardEditOperation, DashboardEditScope, DashboardEditScopeKind,
    ExecutionOutputAddress, ExecutionOutputEditKind, ExecutionOutputEditPhase,
    ExecutionPresentationEdit, ExecutionReportEdit, ExecutionResponseTextEdit,
    ExecutionOutputEditRecord, SdkExecutionRecord, SdkContractRunParameters,
)

from epoch_sdk.extensions import ExecutionExtensionClient
from epoch_sdk.output_validation import TextValue
from epoch_sdk.responses import SavedResearchResponse

pytestmark = pytest.mark.live_run_outputs


def output_version(record: SdkExecutionRecord) -> int:
    assert record.output_revision is not None
    return record.output_revision.version


def accepted_version(record: ExecutionOutputEditRecord) -> int:
    assert record.phase == ExecutionOutputEditPhase.COMPLETED and record.accepted_revision is not None
    return record.accepted_revision.version


def answer_text(answer: SavedResearchResponse | None) -> str:
    assert answer is not None
    part = next(part for part in answer.content.outputs if part.name == "answer")
    assert isinstance(part, TextValue)
    return part.value


def test_real_run_outputs_and_same_execution_edits():
    backend = os.getenv("EPOCH_RUN_OUTPUT_FIXTURE_BACKEND", "")
    ai = os.getenv("EPOCH_RUN_OUTPUT_FIXTURE_AI", "")
    evidence = os.getenv("EPOCH_RUN_OUTPUT_FIXTURE_EVIDENCE", "")
    if not all((backend, ai, evidence)):
        pytest.skip("Explicit loopback Backend/AI fixture origins and evidence directory are required")
    assert backend.startswith("http://127.0.0.1:") and ai.startswith("http://127.0.0.1:")
    root = Path(evidence)
    root.mkdir(parents=True, exist_ok=True)

    def capture(name, value):
        if hasattr(value, "model_dump"):
            value = value.model_dump(mode="json", by_alias=True, exclude_unset=True)
        (root / f"{name}.json").write_text(json.dumps(value, indent=2) + "\n")

    def handle(label):
        return f"acceptance-{label}-{uuid.uuid4().hex}"

    async def scenario():
        async with httpx.AsyncClient(timeout=120) as http:
            client = ExecutionExtensionClient()
            client.backend = AsyncStratifyX(base_url=backend, token="run-output-owner", httpx_client=http)

            async def state(origin):
                reply = await http.get(origin + "/__fixture/state")
                reply.raise_for_status()
                return reply.json()

            async def control(mode="success", delay=0.0):
                reply = await http.put(ai + "/__fixture/control", json={"mode": mode, "delay_seconds": delay})
                reply.raise_for_status()

            async def complete(native):
                deadline = time.monotonic() + 100
                while time.monotonic() < deadline:
                    record = await client.execution_outputs(native.execution_id)
                    if record.response_phase is not None and record.response_phase.value == "outputs_recorded":
                        assert output_version(record) == 1
                        return record
                    assert record.error is None, record
                    await asyncio.sleep(0.05)
                pytest.fail("The real native run did not seal its outputs within the fixture budget")

            async def initial(study="mixed-report", selected_client=client):
                request = CreateSdkExecutionRequest(operation_id=handle(study), study_id=study,
                    source_execution_id="original", input_tables=["orders"], parameters=SdkContractRunParameters())
                record = await selected_client.execute_extension(request)
                if selected_client is client:
                    return await complete(record)
                for _ in range(2000):
                    record = await selected_client.execution_outputs(record.execution_id)
                    if record.output_revision is not None:
                        return record
                    assert record.error is None, record
                    await asyncio.sleep(0.05)
                pytest.fail("The isolated owner's run did not complete")

            await control()
            before, ai_before = await state(backend), await state(ai)
            capture("baseline", {"backend": before, "ai": ai_before})
            first = await initial()
            execution = first.execution_id
            capture("initial", first)
            initial_answer = await client.execution_answer(execution)
            assert initial_answer is not None
            capture("initial-answer", initial_answer)
            assert [part.name for part in initial_answer.content.outputs] == ["numbers", "statistics", "answer"]
            table = await client.response_table(initial_answer.response_id, "numbers", page_size=2)
            table_tail = await client.response_table(initial_answer.response_id, "numbers", offset=2, page_size=2)
            assert table.total_rows == table_tail.total_rows == 4
            assert table.rows[0][2] == table_tail.rows[1][2] == 9007199254740993
            assert table_tail.rows[0][1] is None
            assert (await state(ai))["provider_calls"] == ai_before["provider_calls"] + 1

            for revision, text in ((1, "First manual wording."), (2, "Second manual wording.")):
                request = CreateExecutionOutputEdit(operation_id=handle("manual"), expected_revision=revision,
                    kind=ExecutionOutputEditKind.RESPONSE_TEXT,
                    response_text=[ExecutionResponseTextEdit(name="answer", value=text)])
                receipt = await client.edit_outputs(execution, request)
                assert receipt.phase == ExecutionOutputEditPhase.COMPLETED
                assert accepted_version(receipt) == revision + 1
                assert await client.edit_outputs(execution, request) == receipt
                capture(f"manual-{revision}", receipt)
            # Fresh SDK transport reconstructs current accepted state.
            async with httpx.AsyncClient(timeout=120) as fresh_http:
                fresh = ExecutionExtensionClient()
                fresh.backend = AsyncStratifyX(base_url=backend, token="run-output-owner", httpx_client=fresh_http)
                reread = await fresh.execution_answer(execution)
                assert answer_text(reread) == "Second manual wording."
                assert (await fresh.output_revisions(execution)).total == 3
            assert (await state(ai))["provider_calls"] == ai_before["provider_calls"] + 1
            assert first.extension_outputs is not None
            pin = first.extension_outputs.dashboards[0].presentation
            view = await client.extension_presentation(pin)
            field = next(item for item in view.editable_fields if item.component.kind == DashboardEditComponentKind.MARKDOWN
                         and item.field == DashboardEditField.MARKDOWN)
            note = await client.edit_outputs(execution, CreateExecutionOutputEdit(operation_id=handle("note"),
                expected_revision=3, kind=ExecutionOutputEditKind.PRESENTATION,
                presentation=ExecutionPresentationEdit(execution_category="ALL", scope=DashboardEditScope(kind=DashboardEditScopeKind.FULL_DASHBOARD, references=[]),
                    operations=[DashboardEditOperation(action=DashboardEditAction.SET_TEXT, component=field.component,
                        field=field.field, text="Keep this manual note.")])))
            assert accepted_version(note) == 4
            rewrite = await client.edit_outputs(execution, CreateExecutionOutputEdit(operation_id=handle("rewrite"),
                expected_revision=4, kind=ExecutionOutputEditKind.REPORT,
                report=ExecutionReportEdit(study_id="rewrite-report", input_tables=["numbers"],
                    replace=[ExecutionOutputAddress(response_name="answer")], remove=[])))
            assert rewrite.phase == ExecutionOutputEditPhase.COMPLETED
            assert accepted_version(rewrite) == 5
            capture("rewrite", rewrite)
            assert "\n\n" in answer_text(await client.execution_answer(execution))
            assert (await state(ai))["provider_calls"] == ai_before["provider_calls"] + 2

            derived = await client.edit_outputs(execution, CreateExecutionOutputEdit(operation_id=handle("monthly"),
                expected_revision=5, kind=ExecutionOutputEditKind.REPORT,
                report=ExecutionReportEdit(study_id="monthly-report", input_tables=["numbers"], replace=[
                    ExecutionOutputAddress(response_name="monthly"), ExecutionOutputAddress(execution_category="ALL",
                        component=DashboardEditAddress(kind=DashboardEditComponentKind.CHART, category="Review", id="monthly-totals"))
                ], remove=[])))
            assert derived.phase == ExecutionOutputEditPhase.COMPLETED
            assert accepted_version(derived) == 6
            current = await client.execution_outputs(execution)
            answer = await client.execution_answer(execution)
            assert answer is not None and current.extension_outputs is not None
            monthly = await client.response_table(answer.response_id, "monthly")
            # Independent arithmetic over the explicitly seeded four source rows.
            assert monthly.rows == [["2026-01", 1.25 + 2.75], ["2026-02", 0 - 1.5]]
            accepted_view = await client.extension_presentation(current.extension_outputs.dashboards[0].presentation)
            assert accepted_view.dashboard.content is not None
            assert accepted_view.dashboard.content.markdown[0].markdown == "Keep this manual note."
            assert accepted_view.dashboard.charts[0].id == "monthly-totals"
            capture("monthly", monthly)
            capture("derived", current)
            assert (await state(backend))["runs"] == before["runs"] + 1
            assert (await state(ai))["provider_calls"] == ai_before["provider_calls"] + 2

            await control("timeout")
            failed = await client.edit_outputs(execution, CreateExecutionOutputEdit(operation_id=handle("failed-rewrite"),
                expected_revision=6, kind=ExecutionOutputEditKind.REPORT,
                report=ExecutionReportEdit(study_id="failed-rewrite-report", input_tables=["numbers"],
                    replace=[ExecutionOutputAddress(response_name="answer")], remove=[])))
            assert failed.phase == ExecutionOutputEditPhase.FAILED
            assert failed.candidate_text is not None and failed.text_failures is not None
            assert failed.candidate_text[0].value == "" and failed.text_failures[0].code.value == "text_timeout"
            assert output_version(await client.execution_outputs(execution)) == 6
            capture("failed-rewrite", failed)

            await control()
            # The first reply is deliberately discarded. Reconnect and replay
            # use its original operation identity and cannot create another edit.
            lost_request = CreateExecutionOutputEdit(operation_id=handle("lost-reply"), expected_revision=6,
                kind=ExecutionOutputEditKind.RESPONSE_TEXT, response_text=[ExecutionResponseTextEdit(name="answer", value="Accepted before reconnect.")])
            await client.edit_outputs(execution, lost_request)
            reconnect = await client.output_edit_by_handle(execution, lost_request.operation_id)
            assert accepted_version(reconnect) == 7
            assert await client.edit_outputs(execution, lost_request) == reconnect
            candidates = [CreateExecutionOutputEdit(operation_id=handle("race"), expected_revision=7,
                kind=ExecutionOutputEditKind.RESPONSE_TEXT, response_text=[ExecutionResponseTextEdit(name="answer", value=text)])
                for text in ("Concurrent writer one.", "Concurrent writer two.")]
            raced = await asyncio.gather(*(client.edit_outputs(execution, request) for request in candidates), return_exceptions=True)
            assert sum(not isinstance(item, BaseException) and item.phase == ExecutionOutputEditPhase.COMPLETED for item in raced) == 1
            assert all((isinstance(item, ApiError) and item.status_code == 409) or
                (not isinstance(item, BaseException) and item.phase in {ExecutionOutputEditPhase.COMPLETED, ExecutionOutputEditPhase.CONFLICT}) for item in raced)
            assert output_version(await client.execution_outputs(execution)) == 8

            await control(delay=2.0)
            cancel_request = CreateExecutionOutputEdit(operation_id=handle("cancel"), expected_revision=8,
                kind=ExecutionOutputEditKind.REPORT, report=ExecutionReportEdit(study_id="cancelled-rewrite-report",
                    input_tables=["numbers"], replace=[ExecutionOutputAddress(response_name="answer")], remove=[]))
            pending = asyncio.create_task(client.edit_outputs(execution, cancel_request))
            for _ in range(200):
                try:
                    observed = await client.output_edit_by_handle(execution, cancel_request.operation_id)
                    if observed.phase == ExecutionOutputEditPhase.ACTIVE:
                        break
                except ApiError as error:
                    assert error.status_code == 404
                await asyncio.sleep(0.01)
            else:
                pytest.fail("The controlled candidate was not admitted")
            cancelled = await client.cancel_output_edit(execution, observed.request_id)
            assert cancelled.phase == ExecutionOutputEditPhase.CANCELLED
            assert (await pending).phase == ExecutionOutputEditPhase.CANCELLED
            assert output_version(await client.execution_outputs(execution)) == 8
            capture("cancelled", cancelled)

            await control()
            calls = (await state(ai))["provider_calls"]
            warm = await initial()
            assert warm.execution_id != execution
            assert (await state(ai))["provider_calls"] == calls
            other = ExecutionExtensionClient()
            other.backend = AsyncStratifyX(base_url=backend, token="run-output-other", httpx_client=http)
            with pytest.raises(ApiError) as denied:
                await other.execution_outputs(execution)
            assert denied.value.status_code == 404
            await initial(selected_client=other)
            assert (await state(ai))["provider_calls"] == calls + 1
            await control("timeout")
            empty = await initial("failed-mixed-report")
            empty_answer = await client.execution_answer(empty.execution_id)
            assert answer_text(empty_answer) == ""
            assert empty.extension_outputs is not None and empty.extension_outputs.text_failures is not None
            assert empty.extension_outputs.text_failures[0].code.value == "text_timeout"
            assert empty_answer is not None
            assert (await client.response_table(empty_answer.response_id, "numbers")).total_rows == 4
            capture("model-empty-initial", empty)
            final = await state(backend)
            assert final["original_sha256"] == final["current_original_sha256"] == before["original_sha256"]
            assert (await client.execution_outputs(execution, revision=1)) == first
            capture("history", await client.output_revisions(execution))
            capture("final", {"backend": final, "ai": await state(ai)})
    asyncio.run(scenario())
