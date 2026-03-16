#!/usr/bin/env sh
set -eu

. ./.venv/bin/activate
ruff check qwen_auto_qc tests
ruff format --check qwen_auto_qc tests
