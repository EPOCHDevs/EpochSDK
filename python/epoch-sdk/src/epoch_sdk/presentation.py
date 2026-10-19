"""Plain projections shared by human renderers and nonterminal callers."""

from __future__ import annotations

import json
import re

from .session import NativeUIMessage
from .supervisor import Answer, Question


def ui_text(message: NativeUIMessage) -> str:
    """Render the server's own labels; do not infer research success from them."""
    props = message.props

    def text(key: str) -> str:
        value = props.get(key)
        return value if isinstance(value, str) else ""

    if message.name == "build_study_phase":
        label = text("label") or text("phase")
        detail = text("reason")
        return f"{label} · {text('status')}" + (f" — {detail}" if detail else "")
    if message.name == "build_study_step":
        return text("message")
    if message.name in {"generic_tool_request", "generic_tool_response"}:
        tool = text("tool_name") or "Tool"
        status = text("status")
        detail = text("error_message") or text("params")
        return f"{tool} · {status}" + (f"\n{detail}" if detail else "")
    if message.name == "open_artifact":
        return f"{text('name') or text('type')} · {text('id')}"
    if message.name == "script_chunk":
        return text("code")
    # UI components are service extensions. Keep unfamiliar content inspectable
    # rather than silently hiding it or inventing a second component schema.
    return message.name + "\n" + json.dumps(props, ensure_ascii=False, indent=2)


def question_answer(question: Question, index: int, reply: str) -> Answer:
    """Map explicit 1-based human choices or natural language to native answers."""
    reply = reply.strip()
    if not reply:
        raise ValueError("Choose an option or enter a reply; nothing is selected automatically")
    if reply == "/skip":
        return Answer(question_index=index)
    if re.fullmatch(r"\d+(?:\s*,\s*\d+)*", reply):
        choices = [int(value.strip()) - 1 for value in reply.split(",")]
        if any(choice < 0 or choice >= len(question.options) for choice in choices):
            raise ValueError("Choose one of the displayed option numbers")
        if len(set(choices)) != len(choices):
            raise ValueError("Select each option only once")
        if not question.multi_select and len(choices) != 1:
            raise ValueError("This question accepts one option or a written reply")
        return Answer(question_index=index, selected_indices=choices)
    return Answer(question_index=index, free_form_input=reply)
