#!/usr/bin/env sh
set -eu

WORKSPACE_NAME="${1:?workspace name required}"
RESOURCE_GROUP="${2:?resource group required}"
JOB_SPEC_PATH="${3:-configs/azureml_pipeline_job.yaml}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
JOB_SPEC_ABS="$REPO_ROOT/$JOB_SPEC_PATH"

if [ ! -f "$REPO_ROOT/scripts/azure/prepare_pipeline_inputs.py" ]; then
  echo "Missing required file: scripts/azure/prepare_pipeline_inputs.py" >&2
  exit 1
fi

az ml job create \
  --file "$JOB_SPEC_ABS" \
  --workspace-name "$WORKSPACE_NAME" \
  --resource-group "$RESOURCE_GROUP"
