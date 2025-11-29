#!/usr/bin/env bash
# Build and run a smoke test of the MCP cylera-mcp-server Docker container
# Returns 0 if successful, non-zero if FAILED

IMAGE_NAME="cylera.com/cylera-mcp-server-smoke-test:latest"
read -r -d '' TEST_RPC_MESSAGES <<EOF
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
    {"jsonrpc": "2.0", "method": "notifications/initialized"}
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": { "name": "get_device", "arguments": { "mac_address": "82:32:27:2b:20:8f" }, "_meta": { "progressToken": 0 } } }
EOF

#
# The tests depend on Docker running. Fail fast if it is not.
#
ensure_docker_is_running() {
  if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker daemon not running"
    exit 1
  fi
}

#
# Returns 0 if successful, non-zero if FAILED
#
build_docker_image() {
  docker build -t ${IMAGE_NAME} .
}

#
# Returns 0 if successful, non-zero if FAILED
#
test_docker_image() {
  tmpfile=$(mktemp) || exit 1
  trap "rm -f '$tmpfile'" EXIT
  docker run -i ${IMAGE_NAME} <<<${TEST_RPC_MESSAGES} >"$tmpfile" 2>&1
  grep "Get details about a device by MAC address" $tmpfile >/dev/null
}

#
# First we test the Dockerfile to make sure we can build the image successfuly.
# Next, we run it and simply ensure it responds as expected to sample RPC messages
# over stdin - thereby emulating how an MCP client such as Claude interacts
# with the MCP server.
#
main() {
  ensure_docker_is_running
  build_docker_image
  local result=$?
  if [ "${result}" -eq 0 ]; then
    test_docker_image
    result=$?
  fi
  if [ "${result}" -ne 0 ]; then
    echo "FAILED: Docker container test"
  else
    echo "PASSED: Docker container test"
  fi
  exit $result
}

main "$@"
