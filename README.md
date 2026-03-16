# Qwen AutoQC

This is the Qwen AutoQC pipeline.

The goal is simple:
- take image + label data
- run Qwen on each labeled object
- find labels that look suspicious
- save the results in a clean format
- log runs to MLflow when needed

## What this does

- reads image + label data
- runs Qwen on each object box
- checks if label looks wrong
- saves outputs
- can log to MLflow

## Pipeline flow

1. load config
2. read images and labels
3. extract valid object boxes
4. run Qwen on each object
5. compute QC scores
6. flag possible label issues
7. save outputs
8. log to MLflow if enabled

## Folder structure

Main folders:
- `qwen_auto_qc/`
- `configs/`
- `scripts/`
- `tests/`
- `docs/`
- `azure_devops/`
- `databricks/`

Main code areas:
- `qwen_auto_qc/vlm/` : Qwen model inference
- `qwen_auto_qc/pipeline/` : end-to-end processing
- `qwen_auto_qc/analysis/` : scoring logic
- `qwen_auto_qc/viz/` : visualization hooks

Main entrypoints:
- `run_cli.py`
- `scripts/run_autoqc.py`

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

PowerShell:

```powershell
.\scripts\bootstrap_local.ps1
```

Linux/macOS:

```bash
sh scripts/bootstrap_local.sh
```

Then create `.env` from `.env.example` and set your local paths.

## Run

```bash
python run_cli.py run --config configs/local.yaml
```

Main commands:

- run pipeline
```bash
python run_cli.py run --config configs/local.yaml
```

- benchmark
```bash
python run_cli.py benchmark --config configs/local.yaml
```

- print Azure job spec
```bash
python run_cli.py azureml-spec --config configs/local.yaml
```

- run experiment matrix
```bash
python run_cli.py experiment --config configs/experiment.yaml
```

## Benchmark

```bash
python run_cli.py benchmark --config configs/local.yaml
```

## Tests

```bash
pytest tests --basetemp=pytest_tmp -p no:cacheprovider
```

## Lint

```bash
ruff check src tests
ruff format --check src tests
```

## Type check

```bash
mypy src
```

PowerShell test helper:

```powershell
.\scripts\test_local.ps1
```

Linux/macOS test helper:

```bash
sh scripts/test_local.sh
```

## Containers

Docker build:

```bash
docker build -t qwen-auto-qc:local .
```

Podman build:

```bash
podman build -f Containerfile -t qwen-auto-qc:local .
```

## Outputs

Each run creates a timestamped folder in `runs/`.

Typical files:
- `run_config.json`
- `run_manifest.json`
- `metrics.json`
- `run_summary.json`
- `all_samples.parquet`
- `flagged_samples.parquet`

If parquet is not available, CSV fallback is used.

Monitoring files:
- `run_manifest.json` : current run info + config diff vs previous run
- `run_index.json` : simple history of all runs in `runs/`

## Current status

What is already done:
- package split into smaller modules
- local CLI works
- tests are passing
- Dockerfile and Containerfile are present
- MLflow logging code is present

What still needs real smoke validation:
- actual Qwen inference on local machine
- MLflow end-to-end local run
- Docker/Podman runtime test with real model + data

## Docs

- `docs/architecture.md`
- `docs/config_reference.md`
- `docs/local_run.md`
- `docs/mlflow_local.md`
- `docs/container.md`
- `docs/testing.md`
- `docs/operations.md`
- `docs/production_steps.md`
- `docs/experimentation.md`
