param(
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceName,
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,
    [Parameter(Mandatory = $false)]
    [string]$JobSpecPath = "configs/azureml_job.yaml"
)

$ErrorActionPreference = "Stop"

az ml job create `
    --file $JobSpecPath `
    --workspace-name $WorkspaceName `
    --resource-group $ResourceGroup
