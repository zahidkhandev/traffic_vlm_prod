# Local Run Guide

## Prerequisites
- Python environment with package dependencies installed
- local access to the Qwen3-VL model path configured in `configs/local.yaml`
- `qwen_vl_utils` available in the environment
- local dataset paths for images and labels

## Recommended Smoke-Test Config
Set these values in `configs/local.yaml` first:

```yaml
max_samples: 2
mlflow:
  enabled: false
```

The config expects dataset paths from environment variables:

```bash
AUTOQC_IMAGES_PATH=data/raw/images/test
AUTOQC_LABELS_PATH=data/raw/labels/test
```

Copy `.env.example` to `.env` and set values per developer machine.

## Run
```bash
cd production/qwen_auto_qc
python run_cli.py run --config configs/local.yaml
```

PowerShell:
```powershell
cd production/qwen_auto_qc
.\scripts\run_local.ps1
```

POSIX:
```bash
cd production/qwen_auto_qc
sh scripts/run_local.sh
```

## Outputs
The run writes a timestamped folder under `production/qwen_auto_qc/runs/` with:
- `run_config.json`
- `metrics.json`
- `run_summary.json`
- `all_samples.parquet` or CSV fallback
- `flagged_samples.parquet` or CSV fallback

## Benchmark
```bash
cd production/qwen_auto_qc
python run_cli.py benchmark --config configs/local.yaml
```
