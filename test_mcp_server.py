# These tests depend on data that exists in the demo environment
# CYLERA_BASE_URL="https://partner.demo.cylera.com/"
#
# Test with
# $ uv run pytest -v -s

import pytest
import pytest_asyncio  # Add this import
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from server import mcp


@pytest_asyncio.fixture  # Change this
async def main_mcp_client():
    async with Client(transport=mcp) as mcp_client:
        yield mcp_client


@pytest.mark.asyncio  # Add this decorator
async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    list_tools = await main_mcp_client.list_tools()
    print(list_tools)
    assert len(list_tools) == 7


@pytest.mark.asyncio  # Add this decorator
async def test_get_device(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_device", {"mac_address": "82:32:27:2b:20:8f"}
    )
    device_data = {}
    lines = result.content[0].text.split("\n")
    for line in lines:
        if ":" in line:
            # Split only on the first colon
            key, value = line.split(":", 1)
            key = key.strip("- ").strip()
            value = value.strip()
            device_data[key] = value
        else:
            pass
    assert device_data["hostname"] == "TONNMZDPPS"
