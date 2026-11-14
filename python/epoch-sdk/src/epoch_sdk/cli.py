"""Interactive research CLI over the ordinary Epoch SDK session, and browser sign-in."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import webbrowser
from pathlib import Path

from .contracts import Contract, ErrorResponse, RunRequest
from .errors import EpochError
from .research import EpochClient, ResearchCompleted, ResearchError
from .sign_in import SignInError, SignInSettings, default_store, login, logout


def _has_display() -> bool:
    """Whether a graphical browser can open. Without one, Python's webbrowser may start a text
    browser (lynx, w3m) that takes over this terminal, so only the link is printed."""
    if not sys.platform.startswith("linux"):
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") or os.environ.get("BROWSER"))


def _login(args: argparse.Namespace) -> int:
    settings = SignInSettings.resolve(args.api_url, args.sign_in_domain, args.client_id)
    store = default_store()
    browse = not args.no_browser and _has_display()
    login(settings, store=store, open_browser=webbrowser.open if browse else (lambda _url: None))
    print(f"Signed in to {settings.api_url}. Your sign-in is kept in {store.description}.")
    return 0


def _logout(args: argparse.Namespace) -> int:
    store = default_store()
    signed_in, revoked = logout(args.api_url, store=store)
    if not signed_in:
        print("You weren't signed in.")
    elif revoked:
        print("Signed out. Your sign-in was revoked and removed from this computer.")
    else:
        print("Signed out on this computer. The sign-in service couldn't be reached to revoke "
              "the session, which ends when it expires.")
    return 0


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
    sign_in = commands.add_parser("login", help="Sign in through your browser")
    sign_in.add_argument("--api-url", help="The Epoch API (default: EPOCH_API_URL, then api.epoch.trade)")
    sign_in.add_argument("--sign-in-domain", help="Managed login domain (default: EPOCH_SIGN_IN_DOMAIN)")
    sign_in.add_argument("--client-id", help="Sign-in app client (default: EPOCH_SIGN_IN_CLIENT_ID)")
    sign_in.add_argument("--no-browser", action="store_true", help="Print the sign-in link instead")
    sign_out = commands.add_parser("logout", help="Sign out and forget the stored sign-in")
    sign_out.add_argument("--api-url", help="The Epoch API (default: EPOCH_API_URL, then api.epoch.trade)")
    args = parser.parse_args()
    if args.command in {"login", "logout"}:
        try:
            return _login(args) if args.command == "login" else _logout(args)
        except SignInError as error:
            print(str(error), file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("Sign-in cancelled.", file=sys.stderr)
            return 130
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
