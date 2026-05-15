param(
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceName,
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,
    [Parameter(Mandatory = $false)]
    [string]$JobSpecPath = "configs/azureml_pipeline_job.yaml"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..\..")
$jobSpecResolved = Resolve-Path (Join-Path $repoRoot $JobSpecPath)

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot "scripts\azure\prepare_pipeline_inputs.py"))) {
    throw "Missing required file: scripts/azure/prepare_pipeline_inputs.py"
}

az ml job create `
    --file $jobSpecResolved `
    --workspace-name $WorkspaceName `
    --resource-group $ResourceGroup
