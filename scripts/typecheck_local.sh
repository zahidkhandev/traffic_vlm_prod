#!/usr/bin/env sh
set -eu

. ./.venv/bin/activate
mypy src
