#!/usr/bin/env bash

#
# Run all the tests - returns 0 if all tests PASS
#

./test_docker_container.sh || exit 1
uv run pytest -v || exit 1
uvx ruff check || exit 1
uvx pyright . || exit 1
