# Remote mode: each tool call acts as the person signed in through WorkOS,
# exchanging their WorkOS token for a Cylera token. No network: the
# signed-in person's access token, the token exchange and the Partner API
# are stand-ins, so these run without demo credentials.
#
# Test with
# $ uv run pytest -v test_remote_mode.py

import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from fastmcp.client import Client
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.providers.workos import AuthKitProvider
from mcp.types import TextContent
import cylera_client
import server
from cylera_client import CyleraExchangeError

BASE_URL = "https://partner.example.cylera.com/"
WORKOS_TOKEN = "workos-access-token"  # nosec B105 - placeholder, not a real credential


class PartnerAPI:
    """Stands in for the Partner API: answers GET /organization/ for the
    organization the bearer token was issued for, and queues switches."""

    def __init__(self):
        self.organization_for_token = {}
        self.bearer_tokens = []
        self.switches = []

    def request(self, session, method, url, **kwargs):
        token = session.headers.get("Authorization", "").removeprefix("Bearer ")
        self.bearer_tokens.append(token)
        response = MagicMock(status_code=200)
        response.raise_for_status.return_value = None
        if url.endswith("/organization/switch"):
            self.switches.append(kwargs["params"]["id"])
            response.json.return_value = {"message": "Organization switch queued successfully"}
        else:
            response.json.return_value = {"organization_id": 1, "name": self.organization_for_token[token]}
        return response


@pytest.fixture
def partner_api(monkeypatch):
    api = PartnerAPI()
    monkeypatch.setattr(
        cylera_client.requests.Session, "request", lambda session, method, url, **kw: api.request(session, method, url, **kw)
    )
    return api


class TokenExchange:
    """Stands in for the token exchange: each call mints a new Cylera
    token, for the organization the person is in at that moment."""

    def __init__(self, partner_api):
        self.partner_api = partner_api
        self.calls = []
        self.organization = "Ashton Medical"

    def __call__(self, base_url, workos_token):
        self.calls.append((base_url, workos_token))
        token = f"cylera-token-{len(self.calls)}"
        self.partner_api.organization_for_token[token] = self.organization
        return token


@pytest.fixture
def exchanges(monkeypatch, partner_api):
    exchange = TokenExchange(partner_api)
    monkeypatch.setattr(server, "exchange_workos_token", exchange)
    return exchange


@pytest.fixture
def signed_in(monkeypatch):
    monkeypatch.setattr(server, "remote_base_url", BASE_URL)
    access_token = AccessToken(token=WORKOS_TOKEN, client_id="https://claude.ai/oauth/claude-code-client-metadata", scopes=[])
    monkeypatch.setattr(server, "get_access_token", lambda: access_token)


@pytest_asyncio.fixture
async def mcp_client():
    async with Client(transport=server.mcp) as client:
        yield client


def _text(result) -> str:
    assert isinstance(result.content[0], TextContent)
    return result.content[0].text


@pytest.mark.asyncio
async def test_a_tool_call_acts_as_the_signed_in_person(mcp_client, signed_in, exchanges, partner_api):
    result = await mcp_client.call_tool("get_organization", {})

    assert result.structured_content == {"organization_id": 1, "name": "Ashton Medical"}
    assert exchanges.calls == [(BASE_URL, WORKOS_TOKEN)]
    # The Partner API only ever sees the exchanged Cylera token.
    assert partner_api.bearer_tokens == ["cylera-token-1"]


@pytest.mark.asyncio
async def test_each_tool_call_exchanges_again(mcp_client, signed_in, exchanges):
    await mcp_client.call_tool("get_organization", {})
    await mcp_client.call_tool("get_organization", {})

    assert len(exchanges.calls) == 2


@pytest.mark.asyncio
async def test_a_switch_is_confirmed_with_a_token_from_after_it(mcp_client, signed_in, exchanges, partner_api, monkeypatch):
    def switch_applied(seconds):
        exchanges.organization = "Downton Medical"

    monkeypatch.setattr(server.time, "sleep", switch_applied)

    result = await mcp_client.call_tool(
        "switch_organization", {"organization_id": "mapping-1", "organization_name": "Downton Medical"}
    )

    assert result.structured_content == {"organization_id": 1, "name": "Downton Medical"}
    assert partner_api.switches == ["mapping-1"]
    assert len(exchanges.calls) == 2


@pytest.mark.asyncio
async def test_not_signed_in(mcp_client, monkeypatch):
    monkeypatch.setattr(server, "remote_base_url", BASE_URL)
    monkeypatch.setattr(server, "get_access_token", lambda: None)

    result = await mcp_client.call_tool("get_organization", {}, raise_on_error=False)

    assert result.is_error
    assert _text(result) == "Not signed in to Cylera."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code, message",
    [(401, server.REFUSED_MESSAGE), (404, server.UNSUPPORTED_MESSAGE)],
)
async def test_a_refused_exchange_says_what_to_do(mcp_client, signed_in, partner_api, monkeypatch, status_code, message):
    def refuse(base_url, workos_token):
        raise CyleraExchangeError("refused", status_code)

    monkeypatch.setattr(server, "exchange_workos_token", refuse)

    result = await mcp_client.call_tool("get_organization", {}, raise_on_error=False)

    assert result.is_error
    assert _text(result) == message
    assert partner_api.bearer_tokens == []


@pytest.fixture
def remote_environment(monkeypatch):
    for name in ("CYLERA_USERNAME", "CYLERA_PASSWORD"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(server, "load_dotenv", lambda: None)
    monkeypatch.setenv("CYLERA_BASE_URL", BASE_URL)
    monkeypatch.setenv("WORKOS_AUTHKIT_DOMAIN", "https://example-development.authkit.app")
    monkeypatch.setenv("MCP_PUBLIC_BASE_URL", "http://localhost:8124/")


def test_remote_mode_serves_http_with_authkit(remote_environment, monkeypatch):
    run = MagicMock()
    monkeypatch.setattr(server.mcp, "run", run)
    monkeypatch.setattr(server.mcp, "auth", None)
    monkeypatch.setattr(server, "remote_base_url", None)
    monkeypatch.setattr("sys.argv", ["cylera-mcp-server", "--remote"])

    server.main()

    assert isinstance(server.mcp.auth, AuthKitProvider)
    assert server.remote_base_url == BASE_URL
    run.assert_called_once_with(transport="http", host="127.0.0.1", port=8124, path="/mcp", stateless_http=True)


@pytest.mark.parametrize("variable", ["CYLERA_USERNAME", "CYLERA_PASSWORD"])
def test_remote_mode_refuses_a_stored_password(remote_environment, monkeypatch, variable):
    monkeypatch.setenv(variable, "someone")

    with pytest.raises(SystemExit):
        server._remote_config()


def test_remote_mode_needs_its_settings(remote_environment, monkeypatch):
    monkeypatch.delenv("WORKOS_AUTHKIT_DOMAIN")

    with pytest.raises(SystemExit):
        server._remote_config()


def test_local_mode_is_the_default(monkeypatch):
    run = MagicMock()
    monkeypatch.setattr(server.mcp, "run", run)
    monkeypatch.delenv("CYLERA_MCP_MODE", raising=False)
    monkeypatch.setattr("sys.argv", ["cylera-mcp-server"])

    server.main()

    run.assert_called_once_with(transport="stdio")
    assert server.remote_base_url is None
