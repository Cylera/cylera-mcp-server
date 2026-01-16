# These tests depend on data that exists in the demo environment
# CYLERA_BASE_URL="https://partner.demo.cylera.com/"
#
# Test with
# $ uv run pytest -v -s

import pytest
import pytest_asyncio  # Add this import
import sys
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from mcp.types import TextContent
from server import mcp

# Check if verbose flag is present
VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv


def log(message):
    """Print message only if verbose flag is set"""
    if VERBOSE:
        print(message)


@pytest_asyncio.fixture  # Change this
async def main_mcp_client():
    async with Client(transport=mcp) as mcp_client:
        yield mcp_client


@pytest.mark.asyncio  # Add this decorator
async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    list_tools = await main_mcp_client.list_tools()
    log(list_tools)
    assert len(list_tools) == 8


@pytest.mark.asyncio  # Add this decorator
async def test_get_device(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_device", {"mac_address": "82:32:27:2b:20:8f"}
    )
    device_data = {}
    assert isinstance(result.content[0], TextContent)
    lines = result.content[0].text.split("\n")
    for line in lines:
        if ":" in line:
            # Split only on the first colon
            key, value = line.split(":", 1)
            key = key.strip("- ").strip()
            value = value.strip()
            device_data[key] = value
    assert device_data["hostname"] == "TONNMZDPPS"
