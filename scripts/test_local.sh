#!/usr/bin/env sh
set -eu

. ./.venv/bin/activate
pytest tests --basetemp=pytest_tmp -p no:cacheprovider
