"""Browser sign-in (ENG-2510): PKCE through a real loopback server, stored refresh, renewal, sign-out."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import socket
import stat
import sys
import threading
import urllib.error
import urllib.request
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from epoch_sdk import sign_in as module
from epoch_sdk.sign_in import (
    FileStore,
    KeyringStore,
    SignedInSession,
    SignInError,
    SignInRequired,
    SignInSettings,
    StoredSignIn,
    login,
    logout,
)

API = "https://api.test"
DOMAIN = "https://auth.test"
CLIENT = "cli-client"
SETTINGS = SignInSettings(API, DOMAIN, CLIENT)


def b64(value: object) -> str:
    return base64.urlsafe_b64encode(json.dumps(value).encode()).rstrip(b"=").decode()


class Clock:
    def __init__(self) -> None:
        self.now = 1_800_000_000.0

    def __call__(self) -> float:
        return self.now


class FakeServices:
    """Cognito's token/revoke endpoints and the v1 API's token exchange."""

    def __init__(self, clock: Clock) -> None:
        self.clock = clock
        self.codes: dict[str, tuple[str, str]] = {}
        self.refresh_tokens = {"refresh-1"}
        self.rotate = False
        self.reject_exchange_once = False
        self.exchanged: list[str] = []
        self.refreshes = 0
        self.revoked: list[str] = []

    def jwt(self, lifetime: float = 3600) -> str:
        return f"{b64({'alg': 'none'})}.{b64({'exp': self.clock() + lifetime, 'token_use': 'id'})}.sig"

    def handle(self, request: httpx.Request) -> httpx.Response:
        form = {key: values[0] for key, values in parse_qs(request.content.decode()).items()}
        path = request.url.path
        if request.url.host == "auth.test" and path == "/oauth2/token":
            assert form["client_id"] == CLIENT
            if form["grant_type"] == "authorization_code":
                challenge, redirect = self.codes.pop(form["code"])  # single use
                digest = hashlib.sha256(form["code_verifier"].encode()).digest()
                assert base64.urlsafe_b64encode(digest).rstrip(b"=").decode() == challenge
                assert form["redirect_uri"] == redirect
                return httpx.Response(200, json={"id_token": self.jwt(), "access_token": "cognito-access",
                                                 "refresh_token": "refresh-1", "expires_in": 3600,
                                                 "token_type": "Bearer"})
            assert form["grant_type"] == "refresh_token"
            if form["refresh_token"] not in self.refresh_tokens:
                return httpx.Response(400, json={"error": "invalid_grant"})
            self.refreshes += 1
            body = {"id_token": self.jwt(), "access_token": "cognito-access", "expires_in": 3600}
            if self.rotate:
                self.refresh_tokens = {"refresh-2"}
                body["refresh_token"] = "refresh-2"
            return httpx.Response(200, json=body)
        if request.url.host == "auth.test" and path == "/oauth2/revoke":
            self.revoked.append(form["token"])
            self.refresh_tokens.discard(form["token"])
            return httpx.Response(200)
        if request.url.host == "api.test" and path == "/v1/auth/token":
            assert form["grant_type"] == "urn:ietf:params:oauth:grant-type:token-exchange"
            assert form["subject_token_type"] == "urn:ietf:params:oauth:token-type:id_token"
            if self.reject_exchange_once:
                self.reject_exchange_once = False
                return httpx.Response(401, json={"title": "Unauthorized", "status": 401})
            self.exchanged.append(form["subject_token"])
            return httpx.Response(200, json={"access_token": f"epoch-{len(self.exchanged)}",
                                             "token_type": "Bearer", "expires_in": 900, "scope": "read"})
        return httpx.Response(404)

    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self.handle))


@pytest.fixture
def clock(monkeypatch):
    value = Clock()
    monkeypatch.setattr(module.time, "time", value)
    return value


@pytest.fixture
def services(clock):
    return FakeServices(clock)


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def browser(services: FakeServices, *, states: tuple[str | None, ...] = (None,), error: str | None = None):
    """Plays the user's browser: Cognito redirects back to the loopback with a code."""
    seen: list[str] = []

    def open_browser(url: str) -> None:
        seen.append(url)
        query = {key: values[0] for key, values in parse_qs(urlsplit(url).query).items()}
        services.codes["code-1"] = (query["code_challenge"], query["redirect_uri"])
        callback = urlsplit(query["redirect_uri"])

        def redirect() -> None:
            for state in states:
                params = {"state": state or query["state"]}
                params.update({"error": error} if error else {"code": "code-1"})
                target = f"http://127.0.0.1:{callback.port}{callback.path}?" + "&".join(
                    f"{key}={value}" for key, value in params.items())
                try:
                    urllib.request.urlopen(target, timeout=5).read()
                except urllib.error.HTTPError:
                    pass  # A refused redirect still completes its request.

        threading.Thread(target=redirect, daemon=True).start()

    return open_browser, seen


def test_pkce_verifier_and_s256_challenge():
    verifier, challenge = module._pkce()
    assert len(verifier) == 86 and set(verifier) <= set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")
    digest = hashlib.sha256(verifier.encode()).digest()
    assert challenge == base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def test_login_keeps_only_the_refresh_token_in_a_private_file(tmp_path, services):
    store = FileStore(tmp_path / "epoch" / "credentials.json")
    open_browser, seen = browser(services)
    said: list[str] = []
    record = login(SETTINGS, store=store, open_browser=open_browser, announce=said.append,
                   ports=(free_port(),), timeout=10, http=services.client())
    assert record == StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1")
    authorize = {key: values[0] for key, values in parse_qs(urlsplit(seen[0]).query).items()}
    assert seen[0].startswith(f"{DOMAIN}/oauth2/authorize?")
    assert authorize["response_type"] == "code" and authorize["code_challenge_method"] == "S256"
    assert authorize["scope"] == "openid email" and authorize["redirect_uri"].startswith("http://localhost:")
    # Epoch accepted the sign-in before it was kept.
    assert len(services.exchanged) == 1
    saved = store.path.read_text()
    assert json.loads(saved) == {API: record.model_dump(mode="json")}
    for secret in ("epoch-1", "cognito-access", services.exchanged[0]):
        assert secret not in saved and all(secret not in line for line in said)
    assert "refresh-1" not in "".join(said)
    if os.name == "posix":
        assert stat.S_IMODE(store.path.stat().st_mode) == 0o600
        assert stat.S_IMODE(store.path.parent.stat().st_mode) == 0o700


def test_a_redirect_for_another_sign_in_is_refused_and_the_real_one_accepted(tmp_path, services):
    store = FileStore(tmp_path / "credentials.json")
    open_browser, _ = browser(services, states=("forged", None))
    record = login(SETTINGS, store=store, open_browser=open_browser, announce=lambda _: None,
                   ports=(free_port(),), timeout=10, http=services.client())
    assert record.refresh_token == "refresh-1"


def test_a_declined_or_abandoned_sign_in_stores_nothing(tmp_path, services):
    store = FileStore(tmp_path / "credentials.json")
    open_browser, _ = browser(services, error="access_denied")
    with pytest.raises(SignInError, match="access_denied"):
        login(SETTINGS, store=store, open_browser=open_browser, announce=lambda _: None,
              ports=(free_port(),), timeout=10, http=services.client())
    with pytest.raises(SignInError, match="timed out"):
        login(SETTINGS, store=store, open_browser=lambda _url: None, announce=lambda _: None,
              ports=(free_port(),), timeout=0.2, http=services.client())
    assert not store.path.exists()


def test_the_next_port_is_used_when_one_is_taken(tmp_path, services):
    with socket.socket() as busy:
        busy.bind(("127.0.0.1", 0))
        busy.listen()
        taken = busy.getsockname()[1]
        open_browser, seen = browser(services)
        login(SETTINGS, store=FileStore(tmp_path / "c.json"), open_browser=open_browser,
              announce=lambda _: None, ports=(taken, free_port()), timeout=10, http=services.client())
    redirect = parse_qs(urlsplit(seen[0]).query)["redirect_uri"][0]
    assert urlsplit(redirect).port != taken


def test_tokens_renew_only_as_they_expire(clock, services):
    record = StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1")
    session = SignedInSession(record, http=services.client())
    assert session() == "epoch-1" and services.refreshes == 1
    clock.now += 600
    assert session() == "epoch-1"  # still valid: no network call
    clock.now += 300  # the Epoch token is within its margin; the ID token is not
    assert session() == "epoch-2" and services.refreshes == 1
    clock.now += 3000  # the ID token has lapsed too
    assert session() == "epoch-3" and services.refreshes == 2
    assert "epoch" not in repr(session) and "refresh" not in repr(session)


def test_a_rotated_refresh_token_replaces_the_stored_one(tmp_path, services):
    store = FileStore(tmp_path / "credentials.json")
    record = StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1")
    store.save(record)
    services.rotate = True
    SignedInSession(record, store=store, http=services.client()).access_token()
    stored = store.load(API)
    assert stored is not None and stored.refresh_token == "refresh-2"


def test_an_ended_session_asks_to_sign_in_again(services):
    record = StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="revoked")
    with pytest.raises(SignInRequired, match="epoch login"):
        SignedInSession(record, http=services.client()).access_token()


def test_a_cached_id_token_refused_early_is_refreshed_once_and_retried(clock, services):
    record = StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1")
    session = SignedInSession(record, http=services.client())
    assert session() == "epoch-1" and services.refreshes == 1
    clock.now += 900  # the Epoch token needs renewing; the cached ID token looks valid
    services.reject_exchange_once = True  # but the server already considers it lapsed
    assert session() == "epoch-2" and services.refreshes == 2


def test_logout_revokes_and_forgets(tmp_path, services):
    store = FileStore(tmp_path / "credentials.json")
    store.save(StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1"))
    assert logout(API, store=store, http=services.client()) == (True, True)
    assert services.revoked == ["refresh-1"] and store.load(API) is None
    assert logout(API, store=store, http=services.client()) == (False, False)


def test_logout_forgets_locally_when_revocation_is_unreachable(tmp_path):
    store = FileStore(tmp_path / "credentials.json")
    store.save(StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1"))

    def unreachable(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down", request=request)

    http = httpx.Client(transport=httpx.MockTransport(unreachable))
    assert logout(API, store=store, http=http) == (True, False)
    assert store.load(API) is None


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits")
def test_a_credential_file_others_can_read_is_refused(tmp_path):
    store = FileStore(tmp_path / "credentials.json")
    store.save(StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1"))
    os.chmod(store.path, 0o644)
    with pytest.raises(SignInError, match="other users"):
        store.load(API)


def test_the_keychain_store_keeps_one_entry_per_api():
    class PasswordDeleteError(Exception):
        pass

    class FakeKeyring:
        def __init__(self) -> None:
            self.items: dict[tuple[str, str], str] = {}

        def get_password(self, service: str, name: str) -> str | None:
            return self.items.get((service, name))

        def set_password(self, service: str, name: str, value: str) -> None:
            self.items[(service, name)] = value

        def delete_password(self, service: str, name: str) -> None:
            if self.items.pop((service, name), None) is None:
                raise PasswordDeleteError(name)

    keyring = FakeKeyring()
    store = KeyringStore(keyring)
    record = StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1")
    store.save(record)
    assert list(keyring.items) == [("epoch-sdk", API)]
    assert store.load(API) == record
    store.delete(API)
    store.delete(API)  # nothing stored: not an error
    assert store.load(API) is None


def test_settings_require_https_except_on_this_machine(monkeypatch):
    monkeypatch.delenv("EPOCH_SIGN_IN_DOMAIN", raising=False)
    monkeypatch.delenv("EPOCH_SIGN_IN_CLIENT_ID", raising=False)
    with pytest.raises(SignInError, match="EPOCH_SIGN_IN_DOMAIN"):
        SignInSettings.resolve(API)
    with pytest.raises(SignInError, match="https"):
        SignInSettings.resolve("http://api.example.com", DOMAIN, CLIENT)
    local = SignInSettings.resolve("http://localhost:2024/", DOMAIN + "/", CLIENT)
    assert local == SignInSettings("http://localhost:2024", DOMAIN, CLIENT)


def test_the_file_store_is_chosen_on_request(monkeypatch, tmp_path):
    monkeypatch.setenv("EPOCH_CREDENTIAL_STORE", "file")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    store = module.default_store()
    assert isinstance(store, FileStore) and store.path == tmp_path / "epoch" / "credentials.json"


def test_the_v1_client_uses_the_stored_sign_in_without_an_api_key(monkeypatch, tmp_path):
    from epoch_sdk import Epoch

    monkeypatch.delenv("EPOCH_API_KEY", raising=False)
    monkeypatch.setenv("EPOCH_CREDENTIAL_STORE", "file")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    with pytest.raises(ValueError, match="epoch login"):
        Epoch(api_url=API)
    FileStore().save(StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1"))
    tokens = iter(["epoch-1", "epoch-2"])
    monkeypatch.setattr(SignedInSession, "access_token", lambda self: next(tokens))
    seen: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request.headers["Authorization"])
        return httpx.Response(404, json={"title": "Not found", "status": 404, "code": "NOT_FOUND"})

    epoch = Epoch(api_url=API, http=httpx.Client(transport=httpx.MockTransport(handle)), max_retries=0)
    for _ in range(2):
        with pytest.raises(Exception):
            epoch.research.get("req_1")
    assert seen == ["Bearer epoch-1", "Bearer epoch-2"]  # a fresh token for each call


def test_the_cli_reports_sign_out_without_printing_tokens(monkeypatch, tmp_path, capsys):
    from epoch_sdk import cli

    monkeypatch.setenv("EPOCH_CREDENTIAL_STORE", "file")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["epoch", "logout", "--api-url", API])
    assert cli.main() == 0
    assert "weren't signed in" in capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", ["epoch", "login", "--api-url", API])
    monkeypatch.delenv("EPOCH_SIGN_IN_DOMAIN", raising=False)
    monkeypatch.delenv("EPOCH_SIGN_IN_CLIENT_ID", raising=False)
    assert cli.main() == 1
    assert "EPOCH_SIGN_IN_DOMAIN" in capsys.readouterr().err


def test_an_unusable_keychain_reports_how_to_use_the_file_instead():
    class LockedKeyring:
        def get_password(self, service: str, name: str) -> str | None:
            raise RuntimeError("no Secret Service")

        def set_password(self, service: str, name: str, value: str) -> None:
            raise RuntimeError("no Secret Service")

        def delete_password(self, service: str, name: str) -> None:
            raise RuntimeError("no Secret Service")

    store = KeyringStore(LockedKeyring())
    record = StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1")
    for action in (lambda: store.save(record), lambda: store.load(API), lambda: store.delete(API)):
        with pytest.raises(SignInError, match="EPOCH_CREDENTIAL_STORE=file"):
            action()


def test_a_freshly_signed_in_client_epoch_refuses_is_not_reported_as_an_ended_session(tmp_path, services):
    # The app client isn't enabled at the exchange: say so once, without another refresh.
    store = FileStore(tmp_path / "credentials.json")
    original = services.handle

    def refuse(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/auth/token":
            return httpx.Response(401, json={"title": "Unauthorized", "status": 401,
                                             "detail": "Unknown Cognito client"})
        return original(request)

    services.handle = refuse  # type: ignore[method-assign]
    open_browser, _ = browser(services)
    with pytest.raises(SignInError, match="Unknown Cognito client") as failure:
        login(SETTINGS, store=store, open_browser=open_browser, announce=lambda _: None,
              ports=(free_port(),), timeout=10, http=services.client())
    assert not isinstance(failure.value, SignInRequired)
    assert services.refreshes == 0 and not store.path.exists()


def test_a_non_ascii_state_is_refused_without_breaking_the_sign_in(tmp_path, services):
    open_browser, _ = browser(services, states=("%C3%A9", None))
    record = login(SETTINGS, store=FileStore(tmp_path / "c.json"), open_browser=open_browser,
                   announce=lambda _: None, ports=(free_port(),), timeout=10, http=services.client())
    assert record.refresh_token == "refresh-1"


def test_sign_in_failures_reach_v1_callers_as_api_errors(monkeypatch, tmp_path):
    from epoch_sdk import Epoch, EpochApiError
    from epoch_sdk.sign_in import SignInUnavailable

    monkeypatch.delenv("EPOCH_API_KEY", raising=False)
    monkeypatch.setenv("EPOCH_CREDENTIAL_STORE", "file")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    FileStore().save(StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1"))
    failures = iter([SignInRequired("ended"), SignInUnavailable("down")])

    def fail(self):
        raise next(failures)

    monkeypatch.setattr(SignedInSession, "access_token", fail)
    epoch = Epoch(api_url=API, http=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200))))
    with pytest.raises(EpochApiError) as ended:
        epoch.research.get("req_1")
    assert (ended.value.status, ended.value.code, ended.value.retryable) == (401, "UNAUTHENTICATED", False)
    with pytest.raises(EpochApiError) as down:
        epoch.research.get("req_1")
    assert (down.value.status, down.value.retryable) == (503, True)


def test_the_event_stream_sends_the_signed_in_token_and_close_releases_it(monkeypatch, tmp_path):
    from epoch_sdk import Epoch

    monkeypatch.delenv("EPOCH_API_KEY", raising=False)
    monkeypatch.setenv("EPOCH_CREDENTIAL_STORE", "file")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    FileStore().save(StoredSignIn(api_url=API, domain=DOMAIN, client_id=CLIENT, refresh_token="refresh-1"))
    monkeypatch.setattr(SignedInSession, "access_token", lambda self: "epoch-stream")
    closed: list[bool] = []
    monkeypatch.setattr(SignedInSession, "close", lambda self: closed.append(True))
    seen: list[str] = []
    completed = {"event": "completed", "research": {}}

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request.headers["Authorization"])
        return httpx.Response(200, content=f"data: {json.dumps(completed)}\n\n".encode(),
                              headers={"Content-Type": "text/event-stream"})

    with Epoch(api_url=API, http=httpx.Client(transport=httpx.MockTransport(handle))) as epoch:
        assert [e["event"] for e in epoch.research.events("req_1")] == ["completed"]
    assert seen == ["Bearer epoch-stream"] and closed == [True]


def test_without_a_display_login_only_prints_the_link(monkeypatch):
    from epoch_sdk import cli

    monkeypatch.setattr(cli.sys, "platform", "linux")
    for name in ("DISPLAY", "WAYLAND_DISPLAY", "BROWSER"):
        monkeypatch.delenv(name, raising=False)
    assert not cli._has_display()
    monkeypatch.setenv("DISPLAY", ":0")
    assert cli._has_display()
