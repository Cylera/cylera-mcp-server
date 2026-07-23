#!/usr/bin/env bash

#
# Run all the tests - returns 0 if all tests PASS
#

set -e

USE_DOPPLER=false
USE_OP=false
VERBOSE=false
MIN_OP_VERSION="2.33.0-beta.02"

show_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Run all tests and quality checks for the Cylera MCP server.

Options:
    --use-doppler              Use Doppler secrets management
    --use-op                   Use 1Password CLI secrets management (requires OP_ENVIRONMENT_ID env var)
    --verbose                  Show test output (passes -s to pytest)
    --help                     Show this help message and exit.

Examples:
    $(basename "$0")                                      # Run tests using local .env file
    $(basename "$0") --use-doppler                        # Run tests using Doppler secrets
    OP_ENVIRONMENT_ID=<env-id> $(basename "$0") --use-op  # Run tests using 1Password secrets
    $(basename "$0") --verbose                            # Run tests with output shown
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
  --use-doppler)
    USE_DOPPLER=true
    shift
    ;;
  --use-op)
    USE_OP=true
    shift
    ;;
  --verbose)
    VERBOSE=true
    shift
    ;;
  --help)
    show_help
    exit 0
    ;;
  *)
    echo "Unknown option: $1" >&2
    echo "Use --help for usage information." >&2
    exit 1
    ;;
  esac
done

version_gte() {
  # Returns 0 if $1 >= $2 using version sort
  local version1="$1"
  local version2="$2"
  printf '%s\n%s\n' "$version2" "$version1" | sort -V -C
}

# Check for doppler CLI if --use-doppler was specified
if [[ "$USE_DOPPLER" = true ]] && ! doppler --version >/dev/null 2>&1; then
  echo "Error: Doppler CLI is not installed or not in PATH." >&2
  echo "Please install Doppler CLI: https://docs.doppler.com/docs/install-cli" >&2
  exit 1
fi

# Check for 1Password CLI if --use-op was specified
if [[ "$USE_OP" = true ]]; then
  if ! op --version >/dev/null 2>&1; then
    echo "Error: 1Password CLI (op) is not installed or not in PATH." >&2
    echo "Please install 1Password CLI: https://developer.1password.com/docs/cli/get-started/" >&2
    exit 1
  fi
  installed_op_version=$(op --version)
  if ! version_gte "$installed_op_version" "$MIN_OP_VERSION"; then
    echo "Error: 1Password CLI version $installed_op_version is too old." >&2
    echo "Please upgrade to version $MIN_OP_VERSION or later." >&2
    exit 1
  fi
  if [[ -z "$OP_ENVIRONMENT_ID" ]]; then
    echo "Error: OP_ENVIRONMENT_ID environment variable must be set when using --use-op." >&2
    exit 1
  fi
fi

test_docker_container() {
  if [[ "$USE_DOPPLER" = true ]]; then
    doppler run -- ./test_docker_container.sh || exit 1
  elif [[ "$USE_OP" = true ]]; then
    op run --environment "$OP_ENVIRONMENT_ID" -- ./test_docker_container.sh || exit 1
  else
    ./test_docker_container.sh || exit 1
  fi
}

install_dependencies() {
  uv sync --locked --all-extras --dev
}

run_pytest() {
  PYTEST_ARGS=(-v --cov --cov-report=xml)
  if [[ "$VERBOSE" = true ]]; then
    PYTEST_ARGS+=(-s)
  fi
  if [[ "$USE_DOPPLER" = true ]]; then
    doppler run -- uv run --frozen pytest "${PYTEST_ARGS[@]}" || exit 1
  elif [[ "$USE_OP" = true ]]; then
    op run --environment "$OP_ENVIRONMENT_ID" -- uv run --frozen pytest "${PYTEST_ARGS[@]}" || exit 1
  else
    uv run --frozen pytest "${PYTEST_ARGS[@]}" || exit 1
  fi
}

lint_python() {
  uvx --no-build ruff==0.15.12 check . || exit 1
}

check_types() {
  uvx --no-build pyright==1.1.409 || exit 1
}

lint_shellscripts() {
  shellcheck test_docker_container.sh
  shellcheck test.sh
}

check_app_security() {
  uvx --no-build bandit==1.9.4 -c bandit.yaml ./*.py
}

check_software_supply_chain_security() {
  uv export --no-hashes | uvx --no-build --python 3.13 pip-audit==2.10.0 -r /dev/stdin
}

echo "******** Building and testing a Docker image ************"
test_docker_container
echo "******** Installing dependencies **********"
install_dependencies
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
