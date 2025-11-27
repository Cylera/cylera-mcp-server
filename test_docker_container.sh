#!/usr/bin/env bash
# Build and run a sanity test of the MCP cylera-mcp-server Docker container

docker build -t cylera.com/cylera-mcp-server:latest .
result=$?
if [ "${result}" -eq 0 ]; then
  docker run -i cylera.com/cylera-mcp-server <<EOF >$$.txt 2>&1
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
    {"jsonrpc": "2.0", "method": "notifications/initialized"}
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": { "name": "get_device", "arguments": { "mac_address": "82:32:27:2b:20:8f\n" }, "_meta": { "progressToken": 0 } } }
EOF

  grep "Get details about a device by MAC address" $$.txt >/dev/null
  result=$?
  rm $$.txt
fi
if [ "${result}" -ne 0 ]; then
  echo "FAILED: Docker container test"
else
  echo "PASSED: Docker container test"
fi
exit $result
