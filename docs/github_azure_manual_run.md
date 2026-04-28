# GitHub + Azure Manual Run (No Auto-Deploy Required)

Use this when your repository is private and you cannot grant RBAC for GitHub Actions yet.

## Repo

Current repository:

- `https://github.boschdevcloud.com/NKZ3KOR/AUTOQC_QWEN_BDD100k.git`

## Goal

Run AutoQC in Azure ML while still using GitHub as your source of truth.

## Option A (Recommended): Upload code snapshot from local clone

1. Pull latest code from GitHub locally.
2. In Azure ML job creation, choose **Code source: Local upload**.
3. Upload the project root folder (must contain `run_cli.py` and `configs/azureml.yaml`).
4. Use command:

```bash
python run_cli.py run --config configs/azureml.yaml --images-path ${{inputs.images_path}} --labels-path ${{inputs.labels_path}} --model-path ${{inputs.model_path}}
```

5. Set inputs:
- `images_path`: `autoqc-sandbox-dev-bdd-images-01:1`
- `labels_path`: `autoqc-sandbox-dev-bdd-labels-01:1`
- `model_path`: `qwen-vl-4b`
6. Compute: `autoqc-sandbox-dev-gpu-cluster`
7. Environment variable:
- `MLFLOW_TRACKING_URI=azureml://southindia.api.azureml.ms/mlflow/v1.0/subscriptions/6d35e354-c39e-4f09-8a30-2d71bc4c833e/resourceGroups/rg-autoqc-sandbox-dev/providers/Microsoft.MachineLearningServices/workspaces/ml-autoqc-sandbox-dev`

This gives you reproducible runs without requiring GitHub Actions RBAC changes.

## Option B: Direct private Git source in Azure ML (if supported in your tenant UI)

1. Create a Git/PAT connection in Azure ML.
2. Use repository URL:
- `https://github.boschdevcloud.com/NKZ3KOR/AUTOQC_QWEN_BDD100k.git`
3. Branch: `main`
4. Path: `/`
5. Keep the same command and inputs as Option A.

## Notes

- If model download from Hugging Face is blocked, keep `model_path` as a datastore path and upload model files first.
- If compute is expensive, keep `min nodes=0` and run small smoke tests (`max_samples: 1`) first.
