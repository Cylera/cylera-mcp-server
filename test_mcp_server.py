# These tests depend on data that exists in the demo environment
# CYLERA_BASE_URL="https://partner.demo.cylera.com/"
#
# Test with
# $ uv run pytest -v -s

import json
import pytest
import pytest_asyncio
import sys
from typing import Any
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from mcp.types import TextContent
from server import mcp

VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv


def log(message):
    """Print message only if verbose flag is set"""
    if VERBOSE:
        print(message)


@pytest_asyncio.fixture
async def main_mcp_client():
    async with Client(transport=mcp) as mcp_client:
        yield mcp_client


def parse_json(result) -> Any:
    assert isinstance(result.content[0], TextContent)
    return json.loads(result.content[0].text)


@pytest.mark.asyncio
async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    list_tools = await main_mcp_client.list_tools()
    log(list_tools)
    assert len(list_tools) == 12


@pytest.mark.asyncio
async def test_get_device(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_device", {"mac_address": "82:32:27:2b:20:8f"}
    )
    assert isinstance(result.content[0], TextContent)
    lines = result.content[0].text.split("\n")
    device_data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip("- ").strip()
            value = value.strip()
            device_data[key] = value
    assert device_data["hostname"] == "TONNMZDPPS"


@pytest.mark.asyncio
async def test_get_device_attributes(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_device_attributes", {"mac_address": "7f:14:22:72:00:e5"}
    )
    data = parse_json(result)
    log(data)
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_procedures(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_procedures",
        {"device_uuid": "ffc20dfe-4c24-11ec-8a38-5eeeaabea551", "page_size": 5},
    )
    data = parse_json(result)
    log(data)
    assert "data" in data
    assert "pagination" in data
    pagination = data["pagination"]
    assert "has_more" in pagination
    assert "next_page" in pagination
    assert pagination["page_size"] == 5
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_risk_mitigations(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_risk_mitigations", {"cve_reference": "CVE-2019-0708"}
    )
    assert isinstance(result.content[0], TextContent)
    log(result.content[0].text)
    assert "vulnerability Information" in result.content[0].text


@pytest.mark.asyncio
async def test_get_subnets(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool("get_subnets", {})
    assert isinstance(result.content[0], TextContent)
    log(result.content[0].text)
    assert "Subnets Information" in result.content[0].text


@pytest.mark.asyncio
async def test_get_vulnerabilities(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_vulnerabilities", {"severity": "CRITICAL", "page_size": 5}
    )
    data = parse_json(result)
    log(data)
    assert "data" in data
    assert "pagination" in data
    pagination = data["pagination"]
    assert pagination["page_size"] == 5
    assert "has_more" in pagination
    assert "next_page" in pagination


@pytest.mark.asyncio
async def test_search_for_devices(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "search_for_devices",
        {"vendor": "Philips", "device_type": "X-Ray Machine", "page_size": 5},
    )
    data = parse_json(result)
    log(data)
    assert "data" in data
    assert "pagination" in data
    assert "Philips" in data["data"]


@pytest.mark.asyncio
async def test_get_threats(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool(
        "get_threats", {"severity": "MEDIUM", "page_size": 3}
    )
    data = parse_json(result)
    log(data)
    assert "data" in data
    assert "pagination" in data
    pagination = data["pagination"]
    assert pagination["page_size"] == 3
    assert "has_more" in pagination
    assert "next_page" in pagination


@pytest.mark.asyncio
async def test_get_organization(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool("get_organization", {})
    data = parse_json(result)
    log(data)
    assert "name" in data


@pytest.mark.asyncio
async def test_get_available_organizations(main_mcp_client: Client[FastMCPTransport]):
    result = await main_mcp_client.call_tool("get_available_organizations", {})
    assert not result.is_error
    # Returns an empty list when no org switching is available for this account
    if result.content:
        data = parse_json(result)
        log(data)
        assert isinstance(data, list)
