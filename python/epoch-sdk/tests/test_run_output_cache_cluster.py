"""Opt-in generated-client proof of shared cache, worker restart and expiry.

The launcher owns two actual AI processes and an isolated Redis. Each invocation
of this test records one phase; process restarts/TTL fault injection happen in
the explicit engineering launcher between phases.
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
from stratifyx.types import CreateSdkExecutionRequest, SdkContractRunParameters, SdkExecutionRecord

from epoch_sdk.extensions import ExecutionExtensionClient

pytestmark = pytest.mark.live_run_outputs


def test_run_text_across_ai_processes():
    backend = os.getenv("EPOCH_RUN_OUTPUT_FIXTURE_BACKEND", "")
    ai = os.getenv("EPOCH_RUN_OUTPUT_FIXTURE_AI", "")
    phase = os.getenv("EPOCH_RUN_OUTPUT_CLUSTER_PHASE", "")
    directory = os.getenv("EPOCH_RUN_OUTPUT_FIXTURE_EVIDENCE", "")
    if not all((backend, ai, phase, directory)):
        pytest.skip("An explicit two-worker fixture phase is required")
    assert backend.startswith("http://127.0.0.1:") and ai.startswith("http://127.0.0.1:")
    assert phase in {"cold", "restart", "expiry"}
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)

    async def scenario():
        async with httpx.AsyncClient(timeout=120) as http:
            client = ExecutionExtensionClient()
            client.backend = AsyncStratifyX(base_url=backend, token="run-output-owner", httpx_client=http)

            async def state():
                reply = await http.get(ai + "/__fixture/state")
                reply.raise_for_status()
                return reply.json()

            async def run() -> SdkExecutionRecord:
                request = CreateSdkExecutionRequest(operation_id=f"cluster-{phase}-{uuid.uuid4().hex}",
                    study_id="concurrent-mixed-report", source_execution_id="original", input_tables=["orders"],
                    parameters=SdkContractRunParameters())
                admitted = await client.execute_extension(request)
                deadline = time.monotonic() + 90
                while time.monotonic() < deadline:
                    record = await client.execution_outputs(admitted.execution_id)
                    assert record.error is None, record
                    if record.output_revision is not None:
                        return record
                    await asyncio.sleep(.02)
                pytest.fail("The native cache qualification run did not complete")

            control = await http.put(ai + "/__fixture/control", json={"mode": "success", "delay_seconds": 1.0})
            control.raise_for_status()
            before = (await state())["provider_calls"]
            records = await asyncio.gather(*(run() for _ in range(2 if phase == "cold" else 1)))
            after = (await state())["provider_calls"]
            assert after == before + (0 if phase == "restart" else 1)
            pins = []
            for record in records:
                assert record.output_revision is not None and record.output_revision.version == 1
                assert record.extension_outputs is not None and record.extension_outputs.provenance.commentary
                pins.append(record.extension_outputs.provenance.commentary[0])
            assert len({record.execution_id for record in records}) == len(records)
            assert len({pin.input_sha256 for pin in pins}) == len({pin.result_sha256 for pin in pins}) == 1
            if phase != "cold":
                cold = json.loads((root / "cache-cluster-cold.json").read_text())
                assert pins[0].input_sha256 == cold["input_sha256"]
                assert pins[0].result_sha256 == cold["result_sha256"]
            proof = {"phase": phase, "execution_ids": [record.execution_id for record in records],
                "input_sha256": pins[0].input_sha256, "result_sha256": pins[0].result_sha256,
                "provider_calls_before": before, "provider_calls_after": after,
                "records": [record.model_dump(mode="json", exclude_unset=True) for record in records]}
            (root / f"cache-cluster-{phase}.json").write_text(json.dumps(proof, indent=2) + "\n")
    asyncio.run(scenario())
