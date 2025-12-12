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
    echo "ERROR: Docker daemon not running" >&2
    exit 1
  fi
}

dot_env_help() {
  echo "It needs to contain the following:" >&2
  echo "CYLERA_BASE_URL=https://partner.demo.cylera.com/" >&2
  echo "CYLERA_USERNAME=<username>" >&2
  echo "CYLERA_PASSWORD=<password>" >&2
}
#
# Ensure there is a .env fail available to support
# testing because the .env file is not (should not)
# be part of the Docker image
#
ensure_dot_env_file_exists() {
  if [ -f .env ]; then
    if grep -q "CYLERA_USERNAME" .env &&
      grep -q "CYLERA_PASSWORD" .env &&
      grep -q "CYLERA_BASE_URL" .env; then
      echo "All required variables are present"
    else
      echo "Missing one or more required variables" >&2
      dot_env_help
      exit 1
    fi
  else
    echo ".env file does not exist" >&2
    echo "Unable to test the server without one" >&2
    dot_env_help
    exit 1
  fi
}
#
# Returns 0 if successful, non-zero if FAILED
#
build_docker_image() {
  docker build -t "${IMAGE_NAME}" .
}

#
# Returns 0 if successful, non-zero if FAILED
#
test_docker_image() {
  TMPFILE=$(mktemp) || exit 1
  # shellcheck disable=SC2329
  cleanup() {
    rm -f "$TMPFILE"
  }
  trap cleanup EXIT
  docker run --env-file .env -i "${IMAGE_NAME}" <<<"${TEST_RPC_MESSAGES}" >"$TMPFILE" 2>&1
  grep -q "hostname: TONNMZDPPS" "${TMPFILE}"
}

#
# First we test the Dockerfile to make sure we can build the image successfully.
# Next, we run it and simply ensure it responds as expected to sample RPC messages
# over stdin - thereby emulating how an MCP client such as Claude interacts
# with the MCP server.
#
main() {
  ensure_dot_env_file_exists
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
  exit "$result"
}

main "$@"
