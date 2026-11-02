"""Opt-in real AWS preparation through normal EpochAI, native SDK and stdio MCP.

Use the dedicated review namespace. Create persists identities before any upload
or paid request; verify is read-only and cannot repair/recreate a lost result.
Retain these synthetic resources and receipts for review. No automatic paid retry.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import fcntl
import hashlib
import importlib.metadata
import json
import os
import tempfile
import time
from decimal import Decimal
from pathlib import Path
from typing import Literal
from uuid import uuid4

import pyarrow as pa
from document_read_acceptance import call, identity, loopback, mcp_process, token
from mcp.types import BlobResourceContents, ResourceLink, TextResourceContents
from pyarrow import ipc
from pydantic import BaseModel, ConfigDict, Field
from stratifyx._release import SDK_RELEASE
from stratifyx.core.api_error import ApiError
from stratifyx.types import DatasetBuild, DatasetBuildActionRequest, DatasetBuildRequest

from epoch_sdk.agent_tools import AgentToolsClient

type CaseName = Literal["table", "json", "text", "scalar", "no_match"]


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: CaseName
    request: DatasetBuildRequest
    preparation_ref: str | None = None
    attempt: int | None = None
    dataset_ref: str | None = None
    content_sha256: str | None = None
    confirmed: bool = False


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str = Field(default_factory=lambda: uuid4().hex, pattern=r"^[a-f0-9]{32}$")
    backend_url: str
    graph_url: str
    owner_subject: str
    owner_issuer: str
    file_ref: str
    original_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    native_sdk_version: str = Field(default_factory=lambda: importlib.metadata.version("stratifyx"))
    epoch_sdk_version: str = Field(default_factory=lambda: importlib.metadata.version("epoch-sdk"))
    native_sdk_backend_git_sha: str = SDK_RELEASE["backend_git_sha"]
    cases: list[Case] = Field(default_factory=list)
    checks: list[str] = Field(default_factory=list)

    def persist(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".preparation-evidence-")
        try:
            with os.fdopen(descriptor, "w") as stream:
                stream.write(self.model_dump_json(indent=2) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)


def request(name: CaseName, run: str, file_ref: str) -> DatasetBuildRequest:
    fields = {"period": {"type": "string"}, "revenue": {"type": "number"},
        "unit": {"type": "string"}, "audited": {"type": "boolean"}}
    row = {"type": "object", "additionalProperties": False,
        "properties": fields, "required": list(fields)}
    schema = row
    instruction = "Extract Q3 2026 only. Revenue is USD millions. Preserve period, unit and audited status."
    if name == "table":
        schema = {"type": "object", "additionalProperties": False,
            "properties": {"rows": {"type": "array", "items": row}}, "required": ["rows"]}
    elif name == "text":
        schema = {"type": "string"}
        instruction = 'Return exactly the period label "Q3 2026" from the document as a JSON string.'
    elif name == "scalar":
        schema = {"type": "integer"}
        instruction = "Return only Q3 2026 revenue as an integer in USD millions. Do not return Q2."
    elif name == "no_match":
        instruction = "Extract Q1 2026 revenue only. Do not substitute Q2 or Q3. The absent quarter has no matching records."
    return DatasetBuildRequest.model_validate({
        "request_id": "document-live-" + run + "-" + name,
        "name": "Document review " + name + " " + run[:8],
        "preparation": {"inputs": [{"kind": "file", "file_ref": file_ref}],
            "instruction": instruction, "output_format": "table" if name == "table" else "json",
            "schema_choice": {"mode": "provided", "json_schema_text": json.dumps(schema)},
            "purpose": "knowledge", "enrichment": {"mode": "automatic"}},
    })


def validate_receipt(state: Evidence, *, verify: bool) -> None:
    expected = {"table", "json", "text", "scalar", "no_match"}
    if len(state.cases) != len(expected) or {case.name for case in state.cases} != expected:
        raise ValueError("The receipt must contain exactly the five distinct required cases")
    if state.file_ref != "file:" + state.original_sha256:
        raise ValueError("The receipt original and file identity differ")
    for case in state.cases:
        if case.request != request(case.name, state.run_id, state.file_ref):
            raise ValueError("A recorded request differs from the admitted synthetic case")
        if (case.preparation_ref is None) != (case.attempt is None):
            raise ValueError("An accepted case must retain both its reference and attempt")
        if verify or case.confirmed:
            if not case.confirmed or not case.preparation_ref or not case.attempt or case.attempt < 1:
                raise ValueError("Verify requires every create case to have confirmed its own attempt")
            if case.name == "no_match":
                if case.dataset_ref is not None or case.content_sha256 is not None:
                    raise ValueError("The absent-quarter case cannot contain a saved dataset")
            elif not case.dataset_ref or not case.content_sha256 or len(case.content_sha256) != 64:
                raise ValueError("Verify requires all four exact saved references and content hashes")


async def finished(client: AgentToolsClient, ref: str) -> DatasetBuild:
    deadline = time.monotonic() + 600
    previous = None
    while time.monotonic() < deadline:
        build = await client.document_preparation(ref)
        if build.state != previous:
            print(ref, build.state, flush=True)
            previous = build.state
        if build.state not in {"queued", "preparing", "checking", "saving"}:
            return build
        await asyncio.sleep(2)
    raise TimeoutError("The recorded operation remains pending; reopen its exact reference")


async def scenario(args, state: Evidence) -> None:
    validate_receipt(state, verify=args.mode == "verify")
    bearer = token(args.token_file)
    if identity(bearer) != (state.owner_subject, state.owner_issuer):
        raise ValueError("Use this run's original Cognito owner")
    client = AgentToolsClient.connect(graph_url=args.graph_url, backend_url=args.backend_url, token=bearer)
    directory = args.evidence.parent / ("preparation-" + state.run_id)
    directory.mkdir(mode=0o700, exist_ok=True)
    try:
        if args.mode == "create":
            try:
                await client.file(state.file_ref)
            except ApiError as error:
                if error.status_code != 404:
                    raise
            else:
                raise ValueError("The fixture already exists; use the dedicated empty review namespace")
            original = args.original.read_bytes()
            if hashlib.sha256(original).hexdigest() != state.original_sha256:
                raise ValueError("The original changed after admission; no upload or paid work was started")
            uploaded = await client.upload_file(original, name="Northstar-document-review.pdf", media_type="application/pdf")
            assert uploaded.file_ref == state.file_ref and uploaded.content_sha256 == state.original_sha256
            assert not (await client.current_document_reads(state.file_ref)).items
            assert not (await client.current_document_preparations(state.file_ref)).items
            state.checks.append("upload and metadata started no read or preparation")
            state.persist(args.evidence)
            (directory / "original.pdf").write_bytes(original)
        else:
            uploaded = (await client.file(state.file_ref)).file
            assert uploaded.content_sha256 == state.original_sha256
            if args.mode == "verify":
                assert all(case.confirmed for case in state.cases), "Verify cannot repair an unconfirmed create"
        async with mcp_process(args.backend_url, args.graph_url, bearer) as mcp:
            for case in state.cases:
                if args.mode != "verify" and case.preparation_ref is None:
                    # The JSON case exercises explicit extraction through a real
                    # fresh stdio process; the other cases use the same SDK API.
                    build = DatasetBuild.model_validate(await call(mcp, "epoch_prepare_document_dataset", {
                        "request": case.request.model_dump(mode="json", by_alias=True, exclude_unset=True)
                    })) if case.name == "json" else await client.prepare_document_dataset(case.request)
                    case.preparation_ref, case.attempt = build.preparation_ref, build.attempt
                    state.persist(args.evidence)
                    build = await finished(client, build.preparation_ref)
                else:
                    assert case.preparation_ref and case.attempt
                    build = await client.document_preparation(case.preparation_ref)
                    if args.mode == "resume":
                        build = await finished(client, case.preparation_ref)
                assert build.attempt == case.attempt and build.source.content_sha256 == state.original_sha256
                assert build.request == case.request
                (directory / (case.name + "-build.json")).write_text(build.model_dump_json(indent=2))
                if case.name == "no_match":
                    assert build.state == "no_matches" and build.dataset is None and case.dataset_ref is None
                else:
                    assert build.state == "saved" and build.dataset is not None, build.message
                    saved = build.dataset
                    if args.mode != "verify" and case.dataset_ref is None:
                        case.dataset_ref = saved.dataset_ref
                        case.content_sha256 = saved.descriptor.content_sha256
                        state.persist(args.evidence)
                    assert saved.dataset_ref == case.dataset_ref and saved.descriptor.content_sha256 == case.content_sha256
                    assert saved.name == case.request.name
                    assert (await client.dataset(saved.dataset_ref)) == saved
                    assert any(item.dataset_ref == saved.dataset_ref for item in (await client.list_datasets(query=saved.name)).items)
                    preview = await client.preview_dataset(saved.dataset_ref)
                    assert preview.target.kind == "saved" and preview.target.dataset_ref == saved.dataset_ref
                    raw = await client.download_dataset(saved.dataset_ref, expected_sha256=case.content_sha256)
                    expected = {"period": "Q3 2026", "revenue": Decimal(124), "unit": "USD millions", "audited": True}
                    if case.name == "table":
                        assert preview.content.format == "table"
                        rows = ipc.open_file(pa.BufferReader(raw)).read_all().to_pylist()
                        assert rows == [expected]
                        assert type(rows[0]["audited"]) is bool
                        assert preview.content.offset == 0 and preview.content.total_rows == 1
                        assert not preview.content.requires_download and preview.content.next_cursor is None
                        assert len(preview.content.rows) == 1 and set(preview.content.field_ids) == set(expected)
                        observed = dict(zip(preview.content.field_ids, preview.content.rows[0], strict=True))
                        assert not isinstance(observed["revenue"], bool)
                        assert Decimal(str(observed["revenue"])) == Decimal(124)
                        assert {key: value for key, value in observed.items() if key != "revenue"} == {
                            key: value for key, value in expected.items() if key != "revenue"}
                        assert type(observed["audited"]) is bool
                    else:
                        assert preview.content.format == "json"
                        value = json.loads(raw, parse_float=Decimal)
                        assert preview.content.json_pointer == "" and not preview.content.requires_download
                        assert preview.content.json_text.encode() == raw
                        assert value == (expected if case.name == "json" else "Q3 2026" if case.name == "text" else 124)
                        if case.name == "json":
                            assert type(value["audited"]) is bool
                    evidence_ref = saved.descriptor.evidence_ref
                    assert evidence_ref
                    proof = await client.backend.user_files.get_dataset_evidence(evidence_ref, request_options={"max_retries": 0})
                    assert proof.source_sha256 == state.original_sha256 and proof.file_ref == state.file_ref
                    assert proof.citations and all(citation.quote and citation.page == 1 for citation in proof.citations)
                    assert proof.coverage.processed_pages == [1] and not proof.coverage.unread_pages
                    (directory / (case.name + "-evidence.json")).write_text(proof.model_dump_json(indent=2))
                    (directory / (case.name + (".arrow" if case.name == "table" else ".json"))).write_bytes(raw)
                    linked = await mcp.call_tool("epoch_dataset_content", {"dataset_ref": saved.dataset_ref})
                    assert not linked.is_error and isinstance(linked.content[0], ResourceLink)
                    content = await mcp.read_resource(linked.content[0].uri)
                    if case.name != "table":
                        assert isinstance(content.contents[0], TextResourceContents)
                        assert content.contents[0].text.encode() == raw
                    else:
                        assert isinstance(content.contents[0], BlobResourceContents)
                        assert base64.b64decode(content.contents[0].blob, validate=True) == raw
                reopened = DatasetBuild.model_validate(await call(mcp, "epoch_document_preparation", {"preparation_ref": build.preparation_ref}))
                assert reopened == build
                if args.mode != "verify" and not case.confirmed:
                    await client.act_document_preparation(build.preparation_ref,
                        DatasetBuildActionRequest(action="acknowledge", attempt=build.attempt))
                    case.confirmed = True
                    state.persist(args.evidence)
        state.checks.append("real AWS Table/JSON/text/scalar values and absent Q1, original-page evidence, SDK and fresh MCP content")
        if args.mode == "verify":
            state.checks.append("all recorded attempts, saved references and complete hashes reopened with reads only")
        state.persist(args.evidence)
    finally:
        await client.aclose()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("create", "resume", "verify"))
    parser.add_argument("--backend-url", type=loopback, required=True)
    parser.add_argument("--graph-url", type=loopback, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--original", type=Path)
    parser.add_argument("--run-live-aws", action="store_true")
    args = parser.parse_args()
    args.evidence.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock_path = args.evidence.with_name(args.evidence.name + ".lock")
    with lock_path.open("a") as lock:
        lock_path.chmod(0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another run owns this evidence path; no request was started")
        run(args, parser)


def run(args, parser):
    if args.mode == "resume" and not args.run_live_aws:
        parser.error("Resume requires explicit --run-live-aws for previously unstarted cases")
    if args.mode == "create":
        if not args.run_live_aws or not args.original or args.evidence.exists():
            parser.error("Create requires --run-live-aws, the synthetic --original, and a fresh evidence path")
        raw = args.original.read_bytes()
        if not raw.startswith(b"%PDF-"):
            parser.error("Use the approved synthetic PDF fixture")
        digest = hashlib.sha256(raw).hexdigest()
        subject, issuer = identity(token(args.token_file))
        state = Evidence(backend_url=args.backend_url, graph_url=args.graph_url,
            owner_subject=subject, owner_issuer=issuer, file_ref="file:" + digest, original_sha256=digest)
        state.cases = [Case(name=name, request=request(name, state.run_id, state.file_ref))
            for name in ("table", "json", "text", "scalar", "no_match")]
        state.persist(args.evidence)
    else:
        state = Evidence.model_validate_json(args.evidence.read_bytes())
    if (state.backend_url, state.graph_url) != (args.backend_url, args.graph_url):
        raise ValueError("Use the candidate origins recorded before creation")
    asyncio.run(scenario(args, state))


if __name__ == "__main__":
    main()
