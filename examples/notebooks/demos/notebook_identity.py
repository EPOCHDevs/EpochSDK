"""Obtain only an Epoch bearer token from the local operator's login provider."""

from __future__ import annotations

import json
import os
import subprocess


def identity_token() -> str:
    """Read a static token or ask the configured login helper for a current one.

    The prepared notebook launcher configures a trusted argv list in the
    environment. It uses the owner's normal Epoch login/refresh flow. No shell
    is used, and neither provider output nor credentials appear in exceptions.
    Standalone notebook environments can continue to supply EPOCH_TOKEN alone.
    """
    command = os.environ.get("EPOCH_NOTEBOOK_TOKEN_COMMAND")
    if command:
        try:
            argv = json.loads(command)
        except (TypeError, ValueError):
            raise RuntimeError(
                "The notebook's Epoch login command is invalid."
            ) from None
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(value, str) and value for value in argv)
        ):
            raise RuntimeError(
                "The notebook's Epoch login command must be a JSON argv list."
            )
        try:
            result = subprocess.run(
                argv, capture_output=True, text=True, timeout=30, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "Could not contact the local Epoch login helper. Restore the normal "
                "Epoch login and rerun this setup cell."
            ) from None
        token = result.stdout.strip()
        if result.returncode or not token or any(value.isspace() for value in token):
            raise RuntimeError(
                "The Epoch login needs attention. Sign in through the normal login "
                "flow, then rerun this setup cell."
            )
        return token
    token = os.environ.get("EPOCH_TOKEN")
    if not token:
        raise RuntimeError(
            "Set EPOCH_TOKEN to your Epoch identity token, or use the prepared local "
            "notebook server, which supplies Epoch login to its kernels."
        )
    return token
