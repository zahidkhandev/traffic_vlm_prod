# Qwen AutoQC Notes

## Main flow
1. load config
2. read data
3. run Qwen on boxes
4. score results
5. save outputs
6. log to MLflow if enabled

## Main files
- `qwen_auto_qc/config.py`: typed runtime config
- `qwen_auto_qc/dataset.py`: BDD detection extraction
- `qwen_auto_qc/vlm/classifier.py`: grounding prompt + Qwen3-VL inference
- `qwen_auto_qc/analysis/scoring.py`: thresholding and QC decisions
- `qwen_auto_qc/results.py`: structured artifact writing
- `qwen_auto_qc/pipeline/processor.py`: end-to-end orchestration
- `qwen_auto_qc/mlflow_tracking.py`: MLflow logging

## Run local
```bash
python run_cli.py run --config configs/local.yaml
```

## Output
Each run writes:
- `run_config.json`
- `run_manifest.json`
- `metrics.json`
- `run_summary.json`
- `all_samples.parquet` or CSV fallback
- `flagged_samples.parquet` or CSV fallback

Run tracking:
- `run_manifest.json` stores config hash and config changes vs previous run
- `run_index.json` stores basic history of runs

## MLflow
If enabled, it logs params, metrics, thresholds, and artifacts.

## Current status
- package is split and cleaner now
- tests are passing
- local container files are there
- next real step is local model smoke run + MLflow check
