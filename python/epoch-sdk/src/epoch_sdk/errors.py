"""A domain failure is separate from HTTP/graph transport completion."""

from .contracts import DomainError, ErrorResponse


class EpochError(Exception):
    def __init__(self, error: DomainError, *, execution_id: str | None = None) -> None:
        self.error = error
        self.execution_id = execution_id
        lines = [error.message]
        for gap in error.gaps or []:
            lines.append(f"Missing: {gap.description}")
        for question in error.questions or []:
            text = question.question
            if question.options:
                text += " Options: " + "; ".join(question.options)
            if question.recommended_option:
                text += f". Suggested: {question.recommended_option}"
            lines.append(text)
        if error.recommended_task:
            lines.append(f"Suggested task: {error.recommended_task}")
        super().__init__("\n".join(lines))

    def _render_traceback_(self) -> list[str]:
        """IPython's exception hook: show actionable feedback without SDK frames.

        This changes presentation only. The exception and its original cause
        remain available to Python callers and normal traceback/debugging tools.
        """
        return [f"Epoch · {self.error.code}", str(self)]

    @classmethod
    def from_response(cls, response: ErrorResponse) -> "EpochError":
        return cls(response.error, execution_id=response.execution_id)
