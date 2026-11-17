"""Weekly limits are terminal guidance, separate from retryable rate limiting."""
import json
import sys
import pytest
from pydantic import ValidationError
from epoch_sdk import cli
from epoch_sdk.contracts import DomainError
from epoch_sdk.errors import EpochError


def limit(**changes):
    return DomainError.model_validate({"code": "USAGE_LIMIT_REACHED", "message": "Allowance reached",
        "retryable": False, "meter": "assistant", "resets_at": "2026-11-23T00:00:00Z", **changes})


@pytest.mark.parametrize("change", [{"retryable": True}, {"meter": None}, {"resets_at": "Monday"}])
def test_the_limit_error_requires_terminal_reset_guidance(change):
    with pytest.raises(ValidationError): limit(**change)


@pytest.mark.parametrize("structured", [False, True])
def test_cli_prints_one_reset_line_or_the_requested_json(monkeypatch, capsys, structured):
    async def refuse(_args): raise EpochError(limit())
    monkeypatch.setattr(cli, "_research", refuse)
    monkeypatch.setattr(sys, "argv", ["epoch", "research", "--operation-id", "limit", *(["--json"] if structured else [])])
    assert cli.main() == 1
    output = capsys.readouterr().err.strip()
    if structured:
        assert json.loads(output)["error"] == limit().to_wire()
    else:
        assert output == "You've reached this week's Assistant limit. It resets Mon 23 Nov, 00:00 UTC."
