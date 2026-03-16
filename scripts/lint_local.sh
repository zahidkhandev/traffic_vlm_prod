#!/usr/bin/env sh
set -eu

. ./.venv/bin/activate
ruff check src tests
ruff format --check src tests
