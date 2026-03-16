# Local Run

## Before run
- install deps
- make sure model path is correct in `configs/local.yaml`
- make sure `qwen_vl_utils` works in your env
- make sure image and label paths are set

## Small smoke test
Use small sample count first:

```yaml
max_samples: 2
mlflow:
  enabled: false
```

Set these env vars:

```bash
AUTOQC_IMAGES_PATH=data/raw/images/test
AUTOQC_LABELS_PATH=data/raw/labels/test
```

Best way is copy `.env.example` to `.env` and edit it.

## Run
```bash
python run_cli.py run --config configs/local.yaml
```

PowerShell:
```powershell
.\scripts\run_local.ps1
```

Linux/macOS:
```bash
sh scripts/run_local.sh
```

## Outputs
You will get a new folder under `runs/`.

Main files:
- `run_config.json`
- `run_manifest.json`
- `metrics.json`
- `run_summary.json`
- `all_samples.parquet` or CSV fallback
- `flagged_samples.parquet` or CSV fallback

Monitoring files:
- `run_manifest.json` keeps config hash and config changes vs previous run
- `runs/run_index.json` keeps a simple list of runs

## Benchmark
```bash
cd production/qwen_auto_qc
python run_cli.py benchmark --config configs/local.yaml
```
