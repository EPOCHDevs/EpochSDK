"""Plain projections shared by human renderers and nonterminal callers."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .session import NativeUIMessage
from .supervisor import Answer, Question


class _Projection(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)


class _Chosen(_Projection):
    label: str


class _Selection(_Projection):
    question: str
    chosen: list[_Chosen] = Field(default_factory=list[_Chosen])
    free_form_input: str | None = None
    skipped: bool = False


class _Recap(_Projection):
    selections: list[_Selection]


class _ModelStatus(_Projection):
    # Source: EpochAI common/model_status_ui.py::ModelStatusProps.
    state: Literal[
        "started", "waiting", "retrying", "streaming", "recovered", "failed", "cancelled"
    ]
    optional: bool = False


class _ToolActivity(_Projection):
    # GenericToolUI is emitted under registered tool component names as well
    # as the historical generic_tool_* names. Params/results remain in the
    # headless event; they are not user-facing research narration.
    status: Literal["processing", "success", "error"]
    tool_name: str | None = None
    error_message: str | None = None


def _label(name: str) -> str:
    labels = {
        "discovery": "Discover data",
        "build_study": "Build study",
        "run_study": "Run study",
        "inspect_response_sources": "Inspect saved results",
        "audit_run": "Review results",
        "publish_response": "Publish answer",
    }
    return labels.get(name, name.replace("_", " ").capitalize())


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
    if message.name == "model_status":
        model = _ModelStatus.model_validate(props)
        if model.optional or model.state in {"recovered", "cancelled"}:
            return ""
        return {
            "started": "Thinking…",
            "waiting": "Thinking…",
            "streaming": "Thinking…",
            "retrying": "Waiting for the model service…",
            "failed": "Model call failed",
        }[model.state]
    if message.name == "ask_user_recap":
        recap = _Recap.model_validate(props)
        lines: list[str] = []
        for answer in recap.selections:
            reply = answer.free_form_input or "; ".join(choice.label for choice in answer.chosen)
            if answer.skipped:
                reply = "Skipped"
            if reply:
                lines.append("Reply sent: " + (reply if len(reply) <= 180 else reply[:177] + "…"))
        return "\n".join(lines)
    if text("tool_name") and text("status") in {"processing", "success", "error"}:
        activity = _ToolActivity.model_validate(props)
        state = {"processing": "working", "success": "done", "error": "failed"}[activity.status]
        detail = activity.error_message if activity.status == "error" else None
        return f"{_label(activity.tool_name or message.name)} · {state}" + (
            f" — {detail}" if detail else ""
        )
    if message.name == "open_artifact":
        return text("name") or _label(text("type") or "Study artifact")
    if message.name == "script_chunk":
        return "Authoring study…"
    # Preserve every original property in SessionUI for applications and MCP.
    # Unknown human components get their readable label, never an RPC dump.
    return text("message") or text("label") or _label(message.name)


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
