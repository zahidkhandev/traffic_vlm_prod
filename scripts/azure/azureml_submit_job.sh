#!/usr/bin/env sh
set -eu

WORKSPACE_NAME="${1:?workspace name required}"
RESOURCE_GROUP="${2:?resource group required}"
JOB_SPEC_PATH="${3:-configs/azureml_job.yaml}"

az ml job create \
  --file "$JOB_SPEC_PATH" \
  --workspace-name "$WORKSPACE_NAME" \
  --resource-group "$RESOURCE_GROUP"
