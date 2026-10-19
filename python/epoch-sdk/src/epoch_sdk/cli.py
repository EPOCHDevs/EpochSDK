"""Interactive research CLI over the ordinary Epoch SDK session."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from .contracts import Contract, ErrorResponse, RunRequest
from .errors import EpochError
from .research import EpochClient, ResearchCompleted, ResearchError


async def _research(args: argparse.Namespace) -> int:
    token = os.environ.get("EPOCH_TOKEN") or os.environ.get("EPOCH_ACCESS_TOKEN")
    if not token:
        raise ValueError(
            "Supply your Epoch identity in EPOCH_TOKEN; service/vendor credentials stay on their servers"
        )
    client = EpochClient.connect(
        graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=token,
        assistant_id=os.environ.get("EPOCH_GRAPH_ID", "epoch-ai"),
        ui_url=os.environ.get("EPOCH_UI_URL"),
    )
    try:
        request = (
            None
            if args.request is None
            else RunRequest.model_validate_json(Path(args.request).read_text())
        )
        # CLI auto detection is intentionally terminal-only; a pipe must never
        # open a keyboard prompt, and MCP never invokes this entry point.
        interactive = not args.json and sys.stdin.isatty() and sys.stdout.isatty()
        result = await client.run(
            request,
            operation_id=args.operation_id,
            thread_id=args.thread_id,
            interface="terminal" if interactive else "headless",
        )
        if not interactive:
            wire = (
                result.to_wire()
                if isinstance(result, Contract)
                else result.model_dump(mode="json", by_alias=True)
            )
            print(json.dumps(wire, ensure_ascii=False))
        return 0 if isinstance(result, ResearchCompleted) else 2
    finally:
        await client.aclose()


def main() -> int:
    parser = argparse.ArgumentParser(prog="epoch", description="Epoch research sessions")
    commands = parser.add_subparsers(dest="command", required=True)
    research = commands.add_parser("research", help="Start or reconnect to research")
    research.add_argument("request", nargs="?", help="RunRequest JSON file; omit to reconnect")
    research.add_argument(
        "--operation-id", required=True, help="Readable create-or-attach identity"
    )
    research.add_argument("--thread-id", help="Existing conversation for a new request")
    research.add_argument("--json", action="store_true", help="Structured result, without prompts")
    args = parser.parse_args()
    try:
        return asyncio.run(_research(args))
    except EpochError as error:
        if not args.json and sys.stdin.isatty() and sys.stdout.isatty():
            print(f"Epoch · {error.error.code}\n{error}", file=sys.stderr)
        else:
            failure = (
                error.response
                if isinstance(error, ResearchError)
                else ErrorResponse(error=error.error)
            )
            print(json.dumps(failure.to_wire(), ensure_ascii=False), file=sys.stderr)
        return 1
    except (ValueError, KeyError, OSError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Local session stopped. Reconnect using the same operation ID.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
