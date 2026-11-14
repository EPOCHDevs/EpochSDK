"""Browser sign-in for the SDK, CLI and notebooks (ENG-2510).

``epoch login`` runs OAuth 2.0 authorization code with PKCE (S256) through Cognito's managed login,
with a loopback redirect, and keeps only the Cognito refresh token: in the OS keychain when
``keyring`` is installed, otherwise in a file only you can read. Epoch issues no refresh tokens, so a
signed-in client refreshes its Cognito session and exchanges the new ID token at the v1 API's
``POST /v1/auth/token`` (RFC 8693) for a short-lived Epoch access token. ``epoch logout`` revokes the
refresh token and forgets it.

No token is printed, logged or written anywhere but the credential store.
"""

from __future__ import annotations

import asyncio
import base64
import errno
import hashlib
import json
import os
import secrets
import select
import socket
import stat
import sys
import tempfile
import threading
import time
import webbrowser
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Protocol
from urllib.parse import parse_qs, urlencode, urlsplit

import httpx
from pydantic import BaseModel, ConfigDict, ValidationError

from .api import DEFAULT_API_URL

# Fixed loopback ports, each registered as http://localhost:<port>/callback on the app client:
# Cognito matches callback URLs exactly, so an ephemeral port would be refused.
DEFAULT_PORTS = (53682, 53683, 53684)
SCOPES = "openid email"
# Renew a token this long before it expires, so a request never carries one about to lapse.
EXPIRY_MARGIN = 60.0
TOKEN_EXCHANGE = "urn:ietf:params:oauth:grant-type:token-exchange"
ID_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:id_token"


class SignInError(Exception):
    """Signing in, renewing or signing out failed. The message never contains a token."""


class SignInRequired(SignInError):
    """There is no stored sign-in for this API, or its session has ended."""


class StoredSignIn(BaseModel):
    """What the credential store keeps: the sign-in settings and the Cognito refresh token."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    api_url: str
    domain: str
    client_id: str
    refresh_token: str


@dataclass(frozen=True)
class SignInSettings:
    """Where to sign in: the v1 API, and its Cognito managed login domain and public app client."""

    api_url: str
    domain: str
    client_id: str

    @classmethod
    def resolve(
        cls, api_url: str | None = None, domain: str | None = None, client_id: str | None = None
    ) -> SignInSettings:
        api = _base_url(api_url or os.environ.get("EPOCH_API_URL") or DEFAULT_API_URL, "API URL")
        domain = domain or os.environ.get("EPOCH_SIGN_IN_DOMAIN")
        client_id = client_id or os.environ.get("EPOCH_SIGN_IN_CLIENT_ID")
        if not domain or not client_id:
            raise SignInError(
                "Set EPOCH_SIGN_IN_DOMAIN and EPOCH_SIGN_IN_CLIENT_ID for this API, "
                "or pass --sign-in-domain and --client-id"
            )
        return cls(api, _base_url(domain, "sign-in domain"), client_id)


def _base_url(value: str, label: str) -> str:
    url = value.rstrip("/")
    parts = urlsplit(url)
    local = parts.hostname in {"localhost", "127.0.0.1", "::1"}
    if parts.scheme != "https" and not (parts.scheme == "http" and local):
        raise SignInError(f"The {label} must use https")
    if not parts.hostname or parts.query or parts.fragment:
        raise SignInError(f"The {label} must be a plain base URL")
    return url


# --------------------------------------------------------------------------- credential stores
class CredentialStore(Protocol):
    description: str

    def load(self, api_url: str) -> StoredSignIn | None: ...

    def save(self, record: StoredSignIn) -> None: ...

    def delete(self, api_url: str) -> None: ...


class KeyringStore:
    """The OS keychain (macOS Keychain, Windows Credential Manager, Secret Service) via keyring."""

    SERVICE = "epoch-sdk"

    def __init__(self, keyring: object) -> None:
        self._keyring = keyring
        self.description = "your system keychain"

    def load(self, api_url: str) -> StoredSignIn | None:
        raw = self._keyring.get_password(self.SERVICE, api_url)  # type: ignore[attr-defined]
        return None if raw is None else _record(raw)

    def save(self, record: StoredSignIn) -> None:
        self._keyring.set_password(self.SERVICE, record.api_url, record.model_dump_json())  # type: ignore[attr-defined]

    def delete(self, api_url: str) -> None:
        try:
            self._keyring.delete_password(self.SERVICE, api_url)  # type: ignore[attr-defined]
        except Exception as error:  # keyring.errors.PasswordDeleteError: nothing was stored
            if type(error).__name__ != "PasswordDeleteError":
                raise


class FileStore:
    """A JSON file only you can read, keyed by API URL, for machines without a keychain."""

    def __init__(self, path: Path | None = None) -> None:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
        self.path = path or base / "epoch" / "credentials.json"
        self.description = str(self.path)

    def _read(self) -> dict[str, object]:
        try:
            info = self.path.stat()
        except FileNotFoundError:
            return {}
        if os.name == "posix" and info.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
            raise SignInError(
                f"{self.path} can be read by other users. Delete it and sign in again."
            )
        try:
            data = json.loads(self.path.read_text())
        except ValueError as error:
            raise SignInError(f"{self.path} is not a readable credential file") from error
        if not isinstance(data, dict):
            raise SignInError(f"{self.path} is not a readable credential file")
        return data

    def _write(self, data: dict[str, object]) -> None:
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        # Created private, then renamed over the old file, so it is never briefly readable.
        handle, temporary = tempfile.mkstemp(dir=self.path.parent, prefix=".credentials-")
        try:
            os.chmod(temporary, 0o600)
            with os.fdopen(handle, "w") as file:
                json.dump(data, file)
            os.replace(temporary, self.path)
        except BaseException:
            Path(temporary).unlink(missing_ok=True)
            raise

    def load(self, api_url: str) -> StoredSignIn | None:
        raw = self._read().get(api_url)
        return None if raw is None else _record(json.dumps(raw))

    def save(self, record: StoredSignIn) -> None:
        data = self._read()
        data[record.api_url] = record.model_dump(mode="json")
        self._write(data)

    def delete(self, api_url: str) -> None:
        data = self._read()
        if data.pop(api_url, None) is not None:
            self._write(data)


def _record(raw: str) -> StoredSignIn:
    try:
        return StoredSignIn.model_validate_json(raw)
    except ValidationError as error:
        raise SignInError("The stored sign-in is unreadable. Sign in again.") from error


def default_store() -> CredentialStore:
    """The OS keychain when keyring has a usable backend; otherwise the user-only file.

    Set EPOCH_CREDENTIAL_STORE=file to always use the file.
    """
    if os.environ.get("EPOCH_CREDENTIAL_STORE") == "file":
        return FileStore()
    try:
        import keyring
        from keyring.backends import fail
    except ImportError:
        return FileStore()
    backend = keyring.get_keyring()
    if isinstance(backend, fail.Keyring) or type(backend).__module__.endswith(".null"):
        return FileStore()
    return KeyringStore(keyring)


# --------------------------------------------------------------------------- tokens
def _pkce() -> tuple[str, str]:
    """An RFC 7636 verifier (86 unreserved characters) and its S256 challenge."""
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return verifier, base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _expiry(jwt: str) -> float:
    """A JWT's exp claim, read only to time renewal; the server verifies the token itself."""
    try:
        payload = jwt.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        return float(claims["exp"])
    except (IndexError, ValueError, KeyError, TypeError) as error:
        raise SignInError("The sign-in service returned an unreadable ID token") from error


def _oauth(http: httpx.Client, url: str, form: dict[str, str]) -> dict[str, object]:
    try:
        response = http.post(url, data=form)
    except httpx.HTTPError as error:
        raise SignInError("The sign-in service could not be reached") from error
    if response.status_code == 200:
        try:
            body = response.json()
        except ValueError:
            body = None
        if isinstance(body, dict):
            return body
        raise SignInError("The sign-in service returned an unreadable reply")
    try:
        code = response.json().get("error")
    except (ValueError, AttributeError):
        code = None
    if code == "invalid_grant":
        raise SignInRequired("Your sign-in has ended. Sign in again with `epoch login`.")
    raise SignInError(f"The sign-in service refused the request ({code or response.status_code})")


def _text(body: dict[str, object], key: str) -> str:
    value = body.get(key)
    if not isinstance(value, str) or not value:
        raise SignInError(f"The sign-in service reply has no {key}")
    return value


class SignedInSession:
    """Short-lived Epoch access tokens for a stored sign-in, renewed as they expire.

    Pass the session as a token provider: ``Epoch()`` uses it when it has no API key, and the
    native clients accept ``session.aaccess_token``. It is safe to share between threads.
    """

    def __init__(
        self,
        record: StoredSignIn,
        *,
        store: CredentialStore | None = None,
        http: httpx.Client | None = None,
        id_token: str | None = None,
    ) -> None:
        self.record = record
        self._store = store
        self._http = http or httpx.Client(timeout=30.0)
        self._lock = threading.Lock()
        self._id_token = id_token
        self._id_expires = _expiry(id_token) if id_token else 0.0
        self._access: str | None = None
        self._access_expires = 0.0

    def __repr__(self) -> str:  # Never shows a token.
        return f"SignedInSession(api_url={self.record.api_url!r})"

    def __call__(self) -> str:
        return self.access_token()

    async def aaccess_token(self) -> str:
        return await asyncio.to_thread(self.access_token)

    def access_token(self) -> str:
        with self._lock:
            now = time.time()
            if self._access is not None and self._access_expires - EXPIRY_MARGIN > now:
                return self._access
            if self._id_token is None or self._id_expires - EXPIRY_MARGIN <= now:
                self._refresh()
            if not self._exchange(retry=True):
                self._refresh()
                self._exchange(retry=False)
            assert self._access is not None
            return self._access

    def _refresh(self) -> None:
        tokens = _oauth(self._http, f"{self.record.domain}/oauth2/token", {
            "grant_type": "refresh_token",
            "client_id": self.record.client_id,
            "refresh_token": self.record.refresh_token,
        })
        self._id_token = _text(tokens, "id_token")
        self._id_expires = _expiry(self._id_token)
        rotated = tokens.get("refresh_token")
        if isinstance(rotated, str) and rotated and rotated != self.record.refresh_token:
            self.record = self.record.model_copy(update={"refresh_token": rotated})
            if self._store is not None:
                self._store.save(self.record)

    def _exchange(self, *, retry: bool) -> bool:
        """Swap the ID token for an Epoch access token. False when it was refused and may be retried."""
        assert self._id_token is not None
        try:
            response = self._http.post(f"{self.record.api_url}/v1/auth/token", data={
                "grant_type": TOKEN_EXCHANGE,
                "subject_token": self._id_token,
                "subject_token_type": ID_TOKEN_TYPE,
            })
        except httpx.HTTPError as error:
            raise SignInError("The Epoch API could not be reached") from error
        if response.status_code == 401 and retry:
            return False  # The ID token lapsed early: refresh it once and try again.
        if response.status_code != 200:
            try:
                detail = response.json().get("detail") or response.json().get("title")
            except (ValueError, AttributeError):
                detail = None
            if response.status_code == 401:
                raise SignInRequired("Epoch refused this sign-in. Sign in again with `epoch login`.")
            raise SignInError(f"Epoch refused the sign-in ({detail or response.status_code})")
        try:
            body = response.json()
        except ValueError as error:
            raise SignInError("The Epoch API returned an unreadable token reply") from error
        if not isinstance(body, dict):
            raise SignInError("The Epoch API returned an unreadable token reply")
        self._access = _text(body, "access_token")
        lifetime = body.get("expires_in")
        if not isinstance(lifetime, int) or lifetime < 1:
            raise SignInError("The Epoch API returned a token without a lifetime")
        self._access_expires = time.time() + lifetime
        return True


def stored_session(
    api_url: str | None = None, *, store: CredentialStore | None = None
) -> SignedInSession | None:
    """The stored sign-in for an API, or None when there isn't one."""
    store = store or default_store()
    api = _base_url(api_url or os.environ.get("EPOCH_API_URL") or DEFAULT_API_URL, "API URL")
    record = store.load(api)
    return None if record is None else SignedInSession(record, store=store)


# --------------------------------------------------------------------------- browser sign-in
class _CallbackServer(HTTPServer):
    result: dict[str, str] | None = None
    expected_state: str = ""


class _CallbackServer6(_CallbackServer):
    address_family = socket.AF_INET6


class _Callback(BaseHTTPRequestHandler):
    timeout = 10  # A connection that never sends its request can't stall the sign-in.

    def do_GET(self) -> None:  # noqa: N802 - http.server's handler name
        server = self.server
        assert isinstance(server, _CallbackServer)
        url = urlsplit(self.path)
        if url.path != "/callback":
            self.send_error(404)
            return
        params = {key: values[0] for key, values in parse_qs(url.query).items() if values}
        if not secrets.compare_digest(params.get("state", ""), server.expected_state):
            # Not this sign-in's redirect: refuse it and keep waiting for the real one.
            self._page(400, "This sign-in link doesn't match. Return to your terminal.")
            return
        server.result = params
        if "error" in params:
            self._page(200, "Sign-in was not completed. Return to your terminal.")
        else:
            self._page(200, "You're signed in to Epoch. You can close this tab.")

    def _page(self, status: int, message: str) -> None:
        body = f"<!doctype html><meta charset=utf-8><title>Epoch</title><p>{message}</p>".encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return  # The query carries the authorization code: never log requests.


class _Loopback:
    """Listens on localhost (IPv4 and, when available, IPv6) at the first free registered port."""

    def __init__(self, ports: Sequence[int]) -> None:
        self.servers: list[_CallbackServer] = []
        for port in ports:
            try:
                ipv4 = _CallbackServer(("127.0.0.1", port), _Callback)
            except OSError:
                continue
            try:
                self.servers = [ipv4, _CallbackServer6(("::1", port), _Callback)]
            except OSError as error:
                if error.errno == errno.EADDRINUSE:
                    # Another process holds this port's IPv6 loopback, where a browser may send
                    # the redirect: use the next port.
                    ipv4.server_close()
                    continue
                self.servers = [ipv4]  # No IPv6 loopback: browsers use 127.0.0.1.
            self.port = port
            return
        raise SignInError(f"None of the sign-in ports ({', '.join(map(str, ports))}) is free")

    def wait(self, state: str, timeout: float) -> dict[str, str]:
        for server in self.servers:
            server.expected_state = state
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SignInError("Sign-in timed out. Run `epoch login` again.")
            ready, _, _ = select.select([s.socket for s in self.servers], [], [], remaining)
            for server in self.servers:
                if server.socket in ready:
                    server.handle_request()
                    if server.result is not None:
                        return server.result

    def close(self) -> None:
        for server in self.servers:
            server.server_close()


def _announce(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def login(
    settings: SignInSettings,
    *,
    store: CredentialStore | None = None,
    open_browser: Callable[[str], object] = webbrowser.open,
    announce: Callable[[str], None] = _announce,
    ports: Sequence[int] = DEFAULT_PORTS,
    timeout: float = 300.0,
    http: httpx.Client | None = None,
) -> StoredSignIn:
    """Sign in through the browser, check the sign-in with Epoch, then store it."""
    store = store or default_store()
    owned = http is None
    http = http or httpx.Client(timeout=30.0)
    try:
        return _login(settings, store, open_browser, announce, ports, timeout, http)
    finally:
        if owned:
            http.close()


def _login(
    settings: SignInSettings,
    store: CredentialStore,
    open_browser: Callable[[str], object],
    announce: Callable[[str], None],
    ports: Sequence[int],
    timeout: float,
    http: httpx.Client,
) -> StoredSignIn:
    verifier, challenge = _pkce()
    state = secrets.token_urlsafe(32)
    loopback = _Loopback(ports)
    try:
        redirect_uri = f"http://localhost:{loopback.port}/callback"
        url = f"{settings.domain}/oauth2/authorize?" + urlencode({
            "response_type": "code",
            "client_id": settings.client_id,
            "redirect_uri": redirect_uri,
            "scope": SCOPES,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        })
        announce(f"Opening your browser to sign in to Epoch. If it doesn't open, visit:\n{url}")
        open_browser(url)
        params = loopback.wait(state, timeout)
    finally:
        loopback.close()
    if "error" in params:
        raise SignInError(f"Sign-in was not completed ({params['error']})")
    code = params.get("code")
    if not code:
        raise SignInError("The sign-in redirect carried no authorization code")
    tokens = _oauth(http, f"{settings.domain}/oauth2/token", {
        "grant_type": "authorization_code",
        "client_id": settings.client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": verifier,
    })
    record = StoredSignIn(api_url=settings.api_url, domain=settings.domain,
                          client_id=settings.client_id, refresh_token=_text(tokens, "refresh_token"))
    # Epoch must accept this sign-in before it is kept.
    SignedInSession(record, http=http, id_token=_text(tokens, "id_token")).access_token()
    store.save(record)
    return record


def logout(
    api_url: str | None = None, *, store: CredentialStore | None = None, http: httpx.Client | None = None
) -> tuple[bool, bool]:
    """Revoke and forget the stored sign-in. Returns (was signed in, revoked at the sign-in service)."""
    store = store or default_store()
    api = _base_url(api_url or os.environ.get("EPOCH_API_URL") or DEFAULT_API_URL, "API URL")
    record = store.load(api)
    if record is None:
        return False, False
    owned = http is None
    http = http or httpx.Client(timeout=30.0)
    try:
        response = http.post(f"{record.domain}/oauth2/revoke",
                             data={"token": record.refresh_token, "client_id": record.client_id})
        revoked = response.status_code == 200
    except httpx.HTTPError:
        revoked = False
    finally:
        if owned:
            http.close()
    store.delete(api)
    return True, revoked
