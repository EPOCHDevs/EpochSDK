"""Exercise native operation controllers/CAS with synthetic fixture references.

This is HTTP/component evidence, not a study/model integration run.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import socket
import subprocess
import tempfile
import time
from pathlib import Path

import httpx
from stratifyx import (
    AsyncStratifyX,
    SdkContractRunRequest,
    SdkContractRunParameters,
    SdkResearchLaunch,
    SdkRequestRuntime,
)
from stratifyx._release import SDK_RELEASE
from stratifyx.core.api_error import ApiError

from epoch_sdk.contracts import TableOutputRequest
from epoch_sdk.output_validation import TableValue
from epoch_sdk.responses import ResearchResponseContent, publish_response

OPTIONS = {"max_retries": 0}


async def status(expected, call):
    try:
        await call
    except ApiError as error:
        assert error.status_code == expected, error
        return
    raise AssertionError(f"Expected HTTP {expected}")


async def verify(url: str):
    async with httpx.AsyncClient(timeout=10) as transport:
        owner = AsyncStratifyX(
            base_url=url, token="sdk-fixture-owner", httpx_client=transport
        )
        other = AsyncStratifyX(
            base_url=url, token="sdk-fixture-other", httpx_client=transport
        )
        declaration = TableOutputRequest(
            name="sales",
            type="table",
            schema=[{"name": "year", "type": "int64", "description": "Calendar year"}],
        )
        request = SdkContractRunRequest.model_validate(
            {"task": "Compare sales", "outputs": [declaration.to_wire()]}
        )
        launch = SdkResearchLaunch(assistant_id="epoch-ai")

        async def admit(api=owner.sdk_requests, accepted=request):
            return await api.create_sdk_request(
                request=accepted,
                operation_id="screen-sp500",
                launch=launch,
                request_options=OPTIONS,
            )

        records = await asyncio.gather(*(admit() for _ in range(8)))
        record = records[0]
        assert all(item.request_id == record.request_id for item in records)
        foreign = await admit(other.sdk_requests)
        assert foreign.request_id != record.request_id
        await status(
            404,
            other.sdk_requests.get_sdk_request(
                record.request_id, request_options=OPTIONS
            ),
        )
        await status(
            409,
            admit(
                accepted=SdkContractRunRequest.model_validate(
                    {"task": "Changed task", "outputs": [declaration.to_wire()]}
                )
            ),
        )
        record = await owner.sdk_requests.update_sdk_request(
            record.request_id,
            expected_version=record.version,
            runtime=SdkRequestRuntime(
                thread_id="thread-one",
                assistant_id="epoch-ai",
                execution_ids_before=[],
                outcome_ids_before=[],
            ),
            request_options=OPTIONS,
        )
        record = await owner.sdk_requests.update_sdk_request(
            record.request_id,
            expected_version=record.version,
            graph_run_id="22222222-2222-4222-8222-222222222222",
            request_options=OPTIONS,
        )
        reopened = await owner.sdk_requests.get_sdk_request_by_handle(
            "screen-sp500", request_options=OPTIONS
        )
        assert reopened.graph_run_id == record.graph_run_id
        content = ResearchResponseContent(
            declarations=[declaration],
            outputs=[
                TableValue.model_validate(
                    {
                        "name": "sales",
                        "type": "table",
                        "schema": declaration.to_wire()["schema"],
                        "rows": [["2024"]],
                    }
                )
            ],
        )
        first = await publish_response(
            owner,
            record.request_id,
            content,
            thread_id="thread-one",
            primary_execution_id="native-one",
        )
        # No EpochClient._finish. Publication itself stores the original pin.
        pinned = await owner.sdk_requests.get_sdk_request_by_handle(
            "screen-sp500", request_options=OPTIONS
        )
        assert pinned.response_id == first.response_id and pinned.response_version == 1
        await publish_response(
            owner,
            record.request_id,
            content,
            thread_id="thread-one",
            primary_execution_id="native-one",
            expected_version=1,
        )
        await publish_response(
            owner,
            "later-query",
            content,
            thread_id="thread-one",
            primary_execution_id="native-one",
        )
        pinned = await owner.sdk_requests.get_sdk_request_by_handle(
            "screen-sp500", request_options=OPTIONS
        )
        assert pinned.response_id == first.response_id and pinned.response_version == 1

        parameters = SdkContractRunParameters.model_validate(
            {"period": {"start": "2024-01-01"}}
        )

        async def execute(accepted=parameters):
            return await owner.sdk_requests.create_sdk_execution_request(
                operation_id="refresh-sp500",
                study_id="study-one",
                source_execution_id="native-one",
                parameters=accepted,
                request_options=OPTIONS,
            )

        original = asyncio.create_task(execute())
        deadline = time.monotonic() + 10
        while (
            await transport.get(url + "/__fixture/execution-start-count")
        ).text != "1":
            assert time.monotonic() < deadline
            await asyncio.sleep(0.02)
        original.cancel()
        try:
            await original
        except asyncio.CancelledError:
            pass
        # Fresh transports attach while the disconnected admission is still compiling.
        async with httpx.AsyncClient(timeout=10) as fresh_transport:
            fresh = AsyncStratifyX(
                base_url=url, token="sdk-fixture-owner", httpx_client=fresh_transport
            )
            joined = await fresh.sdk_requests.get_sdk_execution_request_by_handle(
                "refresh-sp500", request_options=OPTIONS
            )
            duplicates = await asyncio.gather(*(execute() for _ in range(8)))
            assert all(item.execution_id == joined.execution_id for item in duplicates)
            while joined.phase.value == "accepted":
                assert time.monotonic() < deadline
                await asyncio.sleep(0.05)
                joined = await fresh.sdk_requests.get_sdk_execution_request_by_handle(
                    "refresh-sp500", request_options=OPTIONS
                )
            assert joined.phase.value == "active"
        assert (
            await transport.get(url + "/__fixture/execution-start-count")
        ).text == "1"
        await status(
            409,
            execute(
                SdkContractRunParameters.model_validate(
                    {"period": {"start": "2025-01-01"}}
                )
            ),
        )
        await status(
            404,
            other.sdk_requests.get_sdk_execution_request_by_handle(
                "refresh-sp500", request_options=OPTIONS
            ),
        )
        return {
            "research_request_id": record.request_id,
            "response_id": first.response_id,
            "pinned_response_version": 1,
            "execution_id": joined.execution_id,
            "concurrent_research_callers": 8,
            "concurrent_execution_callers": 8,
            "execution_starts": 1,
            "original_execution_observer_cancelled": True,
            "owner_isolation": True,
            "changed_inputs_conflict": True,
            "original_pin_after_revision_and_query_advancement": True,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    url = f"http://127.0.0.1:{port}"
    with (
        tempfile.TemporaryDirectory(prefix="epoch-operations-") as temp,
        args.output.with_suffix(".log").open("w") as log,
    ):
        process = subprocess.Popen(
            [str(args.binary.resolve()), str(port), temp], stdout=log, stderr=log
        )
        try:
            deadline = time.monotonic() + 60
            while True:
                assert process.poll() is None, "Native fixture stopped before readiness"
                try:
                    if (
                        httpx.get(
                            url + "/__fixture/execution-start-count", timeout=1
                        ).status_code
                        == 200
                    ):
                        break
                except httpx.HTTPError:
                    pass
                if time.monotonic() > deadline:
                    raise TimeoutError("Native fixture readiness")
                time.sleep(0.1)
            result = asyncio.run(verify(url))
            result.update(
                status="passed",
                evidence="native HTTP and CAS component test",
                real_analysis_proven=False,
                binary_sha256=hashlib.sha256(args.binary.read_bytes()).hexdigest(),
                native_sdk=SDK_RELEASE,
            )
            args.output.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2))
        finally:
            process.terminate()
            process.wait(timeout=15)


if __name__ == "__main__":
    main()
