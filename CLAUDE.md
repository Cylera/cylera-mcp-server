# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for Cylera that provides read-only access to the Cylera Partner API. It enables LLMs to access device inventory, threat information, risk data, and utilization metrics from Cylera's IoT security platform.

## Architecture

The codebase has a simple three-layer architecture:

1. **cylera_client.py**: REST API client for the Cylera Partner API
   - `CyleraClient`: Handles authentication (token-based with auto-refresh) and HTTP requests
   - Helper classes (`Inventory`, `Utilization`, `Network`, `Risk`): Organize API endpoints by domain
   - All API methods return `Dict[str, Any]` containing the raw JSON response from Cylera

2. **server.py**: MCP server implementation using FastMCP
   - Exposes 7 MCP tools that wrap the Cylera API client
   - Formats API responses into human-readable strings or structured dictionaries
   - Tool functions are decorated with `@mcp.tool()` and called by LLM clients

3. **Test files**:
   - `test_cylera_client.py`: Unit tests for the REST API client
   - `test_mcp_server.py`: Component tests that verify the MCP server using a test client

## Development Commands

### Running Tests

All tests depend on the demo environment. Configure `.env` file with:
```
TEST_CYLERA_BASE_URL="https://partner.demo.cylera.com"
CYLERA_BASE_URL="https://partner.demo.cylera.com/"
```

Run all tests:
```bash
uv run pytest -v
```

Run tests with verbose output:
```bash
uv run pytest -v -s
```

Run a single test file:
```bash
uv run pytest -v test_cylera_client.py
```

Run a specific test:
```bash
uv run pytest -v test_cylera_client.py::TestGetDevice::test_get_device
```

Run all tests including Docker smoke test:
```bash
./test.sh
```

### Code Quality

Linting (Ruff):
```bash
uvx ruff check    # Check for issues
uvx ruff format   # Auto-format code
```

Type checking (Pyright):
```bash
uvx pyright .
```

Shell script linting:
```bash
shellcheck *.sh
```

### Security

Scan for vulnerable dependencies:
```bash
uvx pip-audit
```

Update a specific package:
```bash
uv sync --upgrade-package <package-name>
```

### Running the Server Locally

Start the MCP server:
```bash
uv run server.py
```

Debug with MCP Inspector:
```bash
./mcpinspector.sh
```

## Important Implementation Notes

### Authentication Flow
- The `CyleraClient` implements token-based authentication with automatic refresh
- Tokens are cached for 23 hours and automatically renewed when expired
- The `_authenticate()` method uses helper methods `_is_token_valid()` and `_store_token()` to reduce complexity

### API Response Types
- All Cylera API methods return `Dict[str, Any]` (not `List[Dict[str, Any]]`)
- The response dictionary contains a top-level key (e.g., "device", "devices", "vulnerabilities") with the actual data
- Example: `get_device()` returns `{"device": {...}}`, not the device object directly

### MCP Tool Return Types
- Tools that return formatted text for display should return `str`
- Tools that return structured data for LLM processing should return `list[dict]` or `dict`
- The `get_vulnerabilities` tool returns pagination metadata to inform the LLM when more data is available

### Read-Only Design
- This MCP server intentionally supports only GET operations to reduce security risk
- All tools are read-only; no data modification or deletion is possible
- This design prevents data vandalism if the agent is compromised

### Testing Approach
- Tests depend on specific MAC addresses and data in the demo environment
- The `-v` or `--verbose` flag controls test output verbosity via the `VERBOSE` global variable
- MCP server tests use `isinstance(result.content[0], TextContent)` to narrow types for pyright

## Environment Configuration

Required environment variables in `.env`:
- `CYLERA_BASE_URL`: Production Cylera instance URL
- `CYLERA_USERNAME`: Cylera username
- `CYLERA_PASSWORD`: Cylera password
- `TEST_CYLERA_BASE_URL`: Demo environment URL (for tests)
- `TEST_CYLERA_USERNAME`: Demo environment username
- `TEST_CYLERA_PASSWORD`: Demo environment password

Optional debug flag:
- `DEBUG=1`: Enables detailed request/response logging (redacts auth tokens)

## Dependencies

- Python 3.13 (exact version required)
- `uv` for dependency management
- FastMCP for MCP server implementation
- requests for HTTP client
- pytest and pytest-asyncio for testing
