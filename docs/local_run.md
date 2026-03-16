# Local Run

## Before run
- install deps
- create a `.env` file in the project root
- make sure `qwen_vl_utils` works in your env
- make sure dataset is inside `data/raw/`

## Small smoke test
Use small sample count first:

```yaml
max_samples: 2
mlflow:
  enabled: false
```

Keep the dataset inside this project.
Keep the model inside this project too.

Example:
- `models/qwen-vl-4b`
- `data/raw/mini/images/test`
- `data/raw/mini/labels/test`

Create `.env`:

```bash
AUTOQC_MODEL_PATH=models/qwen-vl-4b
AUTOQC_IMAGES_PATH=data/raw/mini/images/test
AUTOQC_LABELS_PATH=data/raw/mini/labels/test
```

`run_cli.py` loads `.env` automatically.

## Run
```bash
python run_cli.py run --config configs/local.yaml
```

Or pass them directly:

```bash
python run_cli.py run --config configs/local.yaml --model-path models/qwen-vl-4b --images-path data/raw/mini/images/test --labels-path data/raw/mini/labels/test
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
python run_cli.py benchmark --config configs/local.yaml
```
