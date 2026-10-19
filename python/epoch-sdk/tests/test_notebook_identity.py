from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

NOTEBOOKS = Path(__file__).resolve().parents[3] / "examples/notebooks"
sys.path.insert(0, str(NOTEBOOKS))

from notebook_identity import identity_token


def test_static_identity_remains_supported(monkeypatch):
    monkeypatch.delenv("EPOCH_NOTEBOOK_TOKEN_COMMAND", raising=False)
    monkeypatch.setenv("EPOCH_TOKEN", "static-test-identity")
    assert identity_token() == "static-test-identity"


def test_login_provider_replaces_the_stale_startup_token(monkeypatch):
    monkeypatch.setenv("EPOCH_TOKEN", "expired-startup-identity")
    monkeypatch.setenv(
        "EPOCH_NOTEBOOK_TOKEN_COMMAND",
        json.dumps([sys.executable, "-c", "print('current-test-identity')"]),
    )
    assert identity_token() == "current-test-identity"


def test_login_failure_never_leaks_provider_output_or_uses_stale_identity(monkeypatch):
    monkeypatch.setenv("EPOCH_TOKEN", "expired-startup-identity")
    monkeypatch.setenv(
        "EPOCH_NOTEBOOK_TOKEN_COMMAND",
        json.dumps(
            [
                sys.executable,
                "-c",
                (
                    "import sys; print('private-fixture-output'); "
                    "print('private-fixture-error', file=sys.stderr); sys.exit(1)"
                ),
            ]
        ),
    )
    with pytest.raises(RuntimeError) as error:
        identity_token()
    assert "private-fixture" not in str(error.value)
    assert "Sign in" in str(error.value)


def test_provider_argv_never_accepts_a_shell_string(monkeypatch):
    monkeypatch.setenv("EPOCH_NOTEBOOK_TOKEN_COMMAND", json.dumps("untrusted-shell-text"))
    with pytest.raises(RuntimeError, match="JSON argv list"):
        identity_token()


def test_provider_timeout_does_not_echo_its_command(monkeypatch):
    monkeypatch.setenv("EPOCH_NOTEBOOK_TOKEN_COMMAND", json.dumps(["fixture-command"]))

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("private-command-detail", 30)

    monkeypatch.setattr(subprocess, "run", timeout)
    with pytest.raises(RuntimeError) as error:
        identity_token()
    assert "private-command-detail" not in str(error.value)
    assert error.value.__cause__ is None
