# Local MLflow Guide

## Enable MLflow
Edit `production/qwen_auto_qc/configs/local.yaml`:

```yaml
mlflow:
  enabled: true
  tracking_uri: ${MLFLOW_TRACKING_URI}
  experiment_name: qwen_auto_qc
  tags:
    algorithm: qwen_full_image_grounding
    platform: local
```

Recommended shared-project alternatives:

1. Leave `tracking_uri` unset and let MLflow use its default local store.
2. Use a repo-relative path such as `file:./mlruns`.
3. Use an environment variable and inject it per developer machine or per container.

Example env-driven pattern:

```bash
set MLFLOW_TRACKING_URI=file:./mlruns
```

## Start UI
```bash
mlflow ui --backend-store-uri ./mlruns
```

## Run Pipeline
```bash
cd production/qwen_auto_qc
python run_cli.py run --config configs/local.yaml
```

## Verify
- one MLflow run appears under `qwen_auto_qc`
- params include model and dataset paths
- metrics include `error_rate` and `mean_latency_ms`
- artifacts include run outputs
