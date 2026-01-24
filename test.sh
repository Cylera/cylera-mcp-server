#!/usr/bin/env bash

#
# Run all the tests - returns 0 if all tests PASS
#

set -e

USE_DOPPLER=false

show_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Run all tests and quality checks for the Cylera MCP server.

Options:
    --use-doppler    Use Doppler secrets management 
    --help           Show this help message and exit.

Examples:
    $(basename "$0")              # Run tests using local .env file
    $(basename "$0") --use-doppler # Run tests using Doppler secrets
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
  --use-doppler)
    USE_DOPPLER=true
    shift
    ;;
  --help)
    show_help
    exit 0
    ;;
  *)
    echo "Unknown option: $1"
    echo "Use --help for usage information."
    exit 1
    ;;
  esac
done

# Check for doppler CLI if --use-doppler was specified
if [ "$USE_DOPPLER" = true ]; then
  if ! doppler --version >/dev/null 2>&1; then
    echo "Error: Doppler CLI is not installed or not in PATH."
    echo "Please install Doppler CLI: https://docs.doppler.com/docs/install-cli"
    exit 1
  fi
fi

test_docker_container() {
  if [ "$USE_DOPPLER" = true ]; then
    doppler run -- ./test_docker_container.sh || exit 1
  else
    ./test_docker_container.sh || exit 1
  fi
}

run_pytest() {
  if [ "$USE_DOPPLER" = true ]; then
    doppler run -- uv run pytest -v || exit 1
  else
    uv run pytest -v || exit 1
  fi
}

lint_python() {
  uvx ruff check || exit 1
}

check_types() {
  uvx pyright . || exit 1
}

lint_shellscripts() {
  shellcheck test_docker_container.sh
  shellcheck test.sh
}

check_app_security() {
  uvx bandit -c bandit.yaml ./*.py
}

check_software_supply_chain_security() {
  uvx pip-audit
}

echo "******** Building and testing a Docker image ************"
test_docker_container
echo "******** Running pytest **********"
run_pytest
echo "******** Running ruff check (linter)  **********"
lint_python
echo "******** Running pyright (checking types) **********"
check_types
echo "******** Running shellcheck (linter) ********"
lint_shellscripts
echo "******** Running bandit (security) *********"
check_app_security
echo "******** Running pip-audit (security scanning packages) *******"
check_software_supply_chain_security
