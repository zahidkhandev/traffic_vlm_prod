# Qwen AutoQC

Production-oriented Qwen3-VL based AutoQC pipeline for BDD-style object labels.

This folder is intended to be runnable as an isolated project from inside
`production/qwen_auto_qc` without depending on root-level project files.
Treat this folder as its own repo root for day-to-day work.

## What It Does
- loads image/label pairs
- extracts valid object detections
- asks Qwen3-VL to classify the object referenced by a grounding box prompt
- computes QC flags from class probabilities
- writes structured run outputs
- optionally logs the run to MLflow

## Local Bootstrap
```bash
cd production/qwen_auto_qc
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

PowerShell helper:
```powershell
cd production/qwen_auto_qc
.\scripts\bootstrap_local.ps1
```

POSIX helper:
```bash
cd production/qwen_auto_qc
sh scripts/bootstrap_local.sh
```

Create a local `.env` from `.env.example` and set shared-project paths there.

## Local Run
```bash
cd production/qwen_auto_qc
python run_cli.py run --config configs/local.yaml
```

## Benchmark
```bash
cd production/qwen_auto_qc
python run_cli.py benchmark --config configs/local.yaml
```

## Tests
```bash
cd production/qwen_auto_qc
pytest tests --basetemp=pytest_tmp -p no:cacheprovider
```

## Lint
```bash
cd production/qwen_auto_qc
ruff check src tests
ruff format --check src tests
```

## Type Check
```bash
cd production/qwen_auto_qc
mypy src
```

PowerShell:
```powershell
cd production/qwen_auto_qc
.\scripts\test_local.ps1
```

POSIX:
```bash
cd production/qwen_auto_qc
sh scripts/test_local.sh
```

## Containers
Docker:
```bash
cd production/qwen_auto_qc
docker build -t qwen-auto-qc:local .
```

Podman:
```bash
cd production/qwen_auto_qc
podman build -f Containerfile -t qwen-auto-qc:local .
```

## Repo-Local Git
This folder can be used as an isolated git root:
```bash
cd production/qwen_auto_qc
git status
```

## Docs
- `docs/production_steps.md`
- `docs/local_run.md`
- `docs/mlflow_local.md`
- `docs/container.md`
