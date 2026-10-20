"""Optional presentation selection; the session core never imports UI libraries."""

from __future__ import annotations

import sys
from typing import Literal

from .research import ResearchCompleted
from .session import EventHandler, ResearchSession
from .supervisor import NeedsInput


def notebook_environment() -> bool:
    try:
        from IPython import get_ipython
    except ImportError:
        return False
    shell = get_ipython()
    return shell is not None and getattr(shell, "kernel", None) is not None


async def run_interactive(
    session: ResearchSession,
    interface: Literal["auto", "terminal", "notebook", "headless"],
    *,
    on_event: EventHandler | None = None,
) -> ResearchCompleted | NeedsInput:
    if interface == "auto":
        interface = (
            "notebook"
            if notebook_environment()
            else ("terminal" if sys.stdin.isatty() and sys.stdout.isatty() else "headless")
        )
    if interface == "headless":
        return await session.run(on_event=on_event)
    if interface == "notebook":
        try:
            from .notebook import NotebookView
        except ImportError as error:
            raise RuntimeError(
                "Install epoch-sdk[notebook] to use the notebook interface"
            ) from error
        return await NotebookView(session).run(on_event=on_event)
    if interface == "terminal":
        if not sys.stdin.isatty():
            raise ValueError(
                "Terminal input is unavailable; use headless mode for structured questions"
            )
        try:
            from .terminal import TerminalView
        except ImportError as error:
            raise RuntimeError(
                "Install epoch-sdk[terminal] to use the terminal interface"
            ) from error
        return await TerminalView(session).run(on_event=on_event)
    raise ValueError("Unknown research interface")
