# Local MLflow

## Turn it on
Edit `configs/local.yaml`:

```yaml
mlflow:
  enabled: true
  tracking_uri: ${MLFLOW_TRACKING_URI}
  experiment_name: qwen_auto_qc
  tags:
    algorithm: qwen_full_image_grounding
    platform: local
```

Set env var:

```bash
set MLFLOW_TRACKING_URI=file:./mlruns
```

## Start UI
```bash
mlflow ui --backend-store-uri ./mlruns
```

## Run Pipeline
```bash
python run_cli.py run --config configs/local.yaml
```

## Verify
- one run should show in experiment `qwen_auto_qc`
- metrics should be there
- artifacts should be there
