#!/usr/bin/env bash

#
# Run all the tests - returns 0 if all tests PASS
#

echo "******** Building and testing a Docker image ************"
./test_docker_container.sh || exit 1
echo "******** Running pytest **********"
uv run pytest -v || exit 1
echo "******** Running ruff check (linter)  **********"
uvx ruff check || exit 1
echo "******** Running pyright (checking types) **********"
uvx pyright . || exit 1
