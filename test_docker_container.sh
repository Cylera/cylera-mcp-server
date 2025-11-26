# This little script just runs a sanity test of the MCP cylera-mcp-server
# when built as a Docker container
docker run -i cylera.com/cylera-mcp-server <<EOF
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
{"jsonrpc": "2.0", "method": "notifications/initialized"}
{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": { "name": "get_device", "arguments": { "mac_address": "82:32:27:2b:20:8f\n" }, "_meta": { "progressToken": 0 } } }
EOF
