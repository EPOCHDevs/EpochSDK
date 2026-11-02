"""Real EpochAI, native SDK and fresh stdio MCP source-reading acceptance.

Use an isolated local Backend storage namespace and running candidate services.
The explicit read uses native UTF-8 processing, so this check needs no paid model
or AWS parsing invocation. The original and read remain available for review;
The cleanup mode removes only this runner's recorded fixture. Login files are
private input and their tokens are never copied into the evidence.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import importlib.metadata
import json
import os
import sys
import tempfile
from collections.abc import Awaitable
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

from mcp import Client
from mcp.client.stdio import StdioServerParameters
from mcp.types import TextContent
from pydantic import BaseModel, ConfigDict, Field
from stratifyx._release import SDK_RELEASE
from stratifyx.core.api_error import ApiError
from stratifyx.types import (
    DocumentContentPage,
    DocumentRead,
    DocumentSearchResponse,
    DocumentSourcePassage,
)

from epoch_sdk.agent_tools import AgentToolsClient


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    backend_url: str
    graph_url: str
    owner_subject: str
    owner_issuer: str
    run_id: str = Field(default_factory=lambda: uuid4().hex, pattern=r"^[a-f0-9]{32}$")
    file_ref: str | None = None
    read_ref: str | None = None
    document_version_ref: str | None = None
    original_sha256: str | None = None
    attempt: int | None = None
    native_sdk_version: str = Field(default_factory=lambda: importlib.metadata.version("stratifyx"))
    epoch_sdk_version: str = Field(default_factory=lambda: importlib.metadata.version("epoch-sdk"))
    native_sdk_backend_git_sha: str = SDK_RELEASE["backend_git_sha"]
    checks: list[str] = Field(default_factory=list)
    cleanup_complete: bool = False

    def persist(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".document-evidence-")
        try:
            with os.fdopen(descriptor, "w") as stream:
                stream.write(self.model_dump_json(indent=2) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)


def loopback(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"} or not parsed.port:
        raise ValueError("Use an explicit local candidate service URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
        raise ValueError("The candidate service URL cannot contain credentials or a path")
    return value.rstrip("/")


def token(path: Path) -> str:
    value = json.loads(path.read_text())["id_token"]
    if not isinstance(value, str) or not value:
        raise ValueError("Use a private current Cognito login file")
    return value


def identity(bearer: str) -> tuple[str, str]:
    # Receipt binding only. Both real services still validate the JWT itself.
    payload = bearer.split(".")[1]
    claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    if not isinstance(claims.get("sub"), str) or not isinstance(claims.get("iss"), str):
        raise TypeError("The login must contain a Cognito subject and issuer")
    return claims["sub"], claims["iss"]


def original_bytes(evidence: Evidence) -> bytes:
    return (f"Synthetic document review {evidence.run_id}\n"
        "Revenue: 9007199254740993\nApproved: false\nExact source text — £124\n").encode()


def mcp_process(backend_url: str, graph_url: str, bearer: str) -> Client:
    allowed = {"PATH", "HOME", "USER", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR"}
    env = {key: value for key, value in os.environ.items() if key in allowed}
    env.update(EPOCH_BACKEND_URL=backend_url, EPOCH_GRAPH_URL=graph_url, EPOCH_TOKEN=bearer)
    return Client(StdioServerParameters(command=sys.executable, args=["-m", "epoch_sdk.mcp"], env=env),
        read_timeout_seconds=60)


async def call(mcp: Client, name: str, arguments: dict) -> dict:
    result = await mcp.call_tool(name, arguments)
    assert not result.is_error, f"MCP operation failed: {name}"
    if result.structured_content is not None:
        return result.structured_content
    assert result.content and isinstance(result.content[0], TextContent)
    return json.loads(result.content[0].text)


async def scenario(args: argparse.Namespace, evidence: Evidence) -> None:
    bearer = token(args.token_file)
    if identity(bearer) != (evidence.owner_subject, evidence.owner_issuer):
        raise ValueError("Reopen and cleanup require this run's original Cognito owner")
    original = original_bytes(evidence)
    digest = hashlib.sha256(original).hexdigest()
    if evidence.file_ref != "file:" + digest or evidence.original_sha256 != digest:
        raise ValueError("The receipt does not identify this runner's deterministic synthetic original")
    client = AgentToolsClient.connect(graph_url=args.graph_url, backend_url=args.backend_url, token=bearer)
    try:
        if args.mode == "cleanup":
            if evidence.cleanup_complete:
                return
            if evidence.file_ref:
                try:
                    reads = (await client.current_document_reads(evidence.file_ref)).items
                except ApiError as error:
                    if error.status_code != 404:
                        raise
                    reads = []
                async def remove(operation: Awaitable[None]) -> None:
                    try:
                        await operation
                    except ApiError as error:
                        if error.status_code != 404:
                            raise
                for row in reads:
                    await remove(client.delete_document_read(row.read_ref))
                await remove(client.delete_file(evidence.file_ref))
            evidence.cleanup_complete = True
            evidence.persist(args.evidence)
            return

        if args.mode == "create":
            uploaded = await client.upload_file(original, name=f"Document-review-{evidence.run_id}.txt",
                media_type="text/plain; charset=utf-8")
        else:
            uploaded = (await client.file(evidence.file_ref)).file
        assert uploaded.content_sha256 == digest and uploaded.file_ref == "file:" + digest
        await client.file(uploaded.file_ref)
        assert any(row.file_ref == uploaded.file_ref for row in (await client.list_files(query=evidence.run_id)).items)
        if args.mode == "create":
            current = await client.current_document_reads(uploaded.file_ref)
            assert not current.items, "Metadata browsing unexpectedly initiated source processing"
            evidence.checks.append("metadata does not start processing")
            evidence.persist(args.evidence)
            operation = await client.start_document_read(uploaded.file_ref)
            evidence.read_ref, evidence.document_version_ref = operation.read_ref, operation.document_version_ref
            evidence.attempt = operation.attempt
            evidence.persist(args.evidence)
        else:
            assert evidence.read_ref and evidence.document_version_ref and evidence.attempt is not None, (
                "The original create did not confirm a result; review its current operation or clean up. "
                "Verify never creates a replacement read."
            )
            operation = await client.document_read(evidence.read_ref)
            assert operation.read_ref == evidence.read_ref and operation.attempt == evidence.attempt
            assert operation.document_version_ref == evidence.document_version_ref
        assert operation.state == "ready" and operation.document_version_ref
        assert operation.source.file_ref == evidence.file_ref and operation.source.content_sha256 == digest
        content = await client.document_content(operation.document_version_ref, limit=100)
        assert content.source.content_sha256 == digest and content.provider_version == "utf8-v1"
        assert not content.has_more and content.total_blocks == len(content.blocks)
        assert "".join(block.text for block in content.blocks).encode() == original
        assert all(block.page is None and block.layer == "primary" for block in content.blocks)
        block = content.blocks[0]
        passage = await client.document_passage(operation.document_version_ref, block.block_ref)
        assert passage.block == block and passage.source.content_sha256 == digest
        search = await client.search_documents(evidence.run_id, file_refs=[uploaded.file_ref])
        assert search.prepared_count == 1 and search.unprepared_count == 0 and search.matches
        replay = await client.start_document_read(uploaded.file_ref) if args.mode == "create" else await client.document_read(operation.read_ref)
        assert replay.read_ref == operation.read_ref and replay.attempt == operation.attempt
        for check in ["explicit EpochAI read persists exact native UTF-8",
            "source version, literal search and passage resolve exact original", "reopen preserves the same attempt"]:
            if check not in evidence.checks:
                evidence.checks.append(check)
        if args.mode == "verify":
            evidence.checks.append("recorded refs, hash and attempt reopened using reads only")
        evidence.persist(args.evidence)

        async with mcp_process(args.backend_url, args.graph_url, bearer) as mcp:
            reopened = DocumentRead.model_validate(await call(mcp, "epoch_document_read", {"read_ref": operation.read_ref}))
            page = DocumentContentPage.model_validate(await call(mcp, "epoch_read_documents", {
                "document_version_ref": operation.document_version_ref, "limit": 100}))
            source = DocumentSourcePassage.model_validate(await call(mcp, "epoch_document_passage", {
                "document_version_ref": operation.document_version_ref, "block_ref": block.block_ref}))
            matches = DocumentSearchResponse.model_validate(await call(mcp, "epoch_search_documents", {
                "query": evidence.run_id, "file_refs": [uploaded.file_ref]}))
            assert reopened == operation and page == content and source == passage and matches == search
        evidence.checks.append("fresh stdio MCP returns the same native operation, source bytes, search and passage")
        evidence.persist(args.evidence)

        if args.foreign_token_file:
            foreign_token = token(args.foreign_token_file)
            assert identity(foreign_token) != (evidence.owner_subject, evidence.owner_issuer), "Use a distinct foreign Cognito identity"
            other = AgentToolsClient.connect(graph_url=args.graph_url, backend_url=args.backend_url, token=foreign_token)
            try:
                for read in (lambda: other.file(uploaded.file_ref),
                    lambda: other.document_read(operation.read_ref),
                    lambda: other.document_content(operation.document_version_ref),
                    lambda: other.document_passage(operation.document_version_ref, block.block_ref)):
                    try:
                        await read()
                    except ApiError as error:
                        assert error.status_code == 404
                    else:
                        raise AssertionError("A foreign owner could read private source content")
                assert not (await other.search_documents(evidence.run_id)).matches
            finally:
                await other.aclose()
            evidence.checks.append("foreign Cognito owner cannot read/search the original, operation or passages")
            evidence.persist(args.evidence)
    finally:
        await client.aclose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("create", "verify", "cleanup"))
    parser.add_argument("--backend-url", type=loopback, required=True)
    parser.add_argument("--graph-url", type=loopback, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--foreign-token-file", type=Path)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "create":
        if args.evidence.exists():
            parser.error("Create requires a fresh evidence path; use verify or cleanup for this recorded run")
        owner, issuer = identity(token(args.token_file))
        evidence = Evidence(backend_url=args.backend_url, graph_url=args.graph_url,
            owner_subject=owner, owner_issuer=issuer)
        evidence.original_sha256 = hashlib.sha256(original_bytes(evidence)).hexdigest()
        evidence.file_ref = "file:" + evidence.original_sha256
        # Record cleanup authority before an upload can commit or lose its ACK.
        evidence.persist(args.evidence)
    else:
        if not args.evidence.exists():
            parser.error("Verify and cleanup require this runner's existing evidence file")
        evidence = Evidence.model_validate_json(args.evidence.read_bytes())
        if evidence.cleanup_complete and args.mode != "cleanup":
            parser.error("This run is retired; create a new run with a fresh evidence path")
    if evidence.backend_url != args.backend_url or evidence.graph_url != args.graph_url:
        parser.error("Reopen and cleanup must use the same isolated service origins as the recorded run")
    asyncio.run(scenario(args, evidence))
    print(json.dumps({"passed_checks": evidence.checks, "cleanup_complete": evidence.cleanup_complete}))


if __name__ == "__main__":
    main()
