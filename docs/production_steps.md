# Qwen AutoQC Production Steps

## Architecture
The production package lives under `production/qwen_auto_qc/` and is isolated from the experiment scripts in `data_clean/confident_learning/`.

Core flow:
1. Load typed run config.
2. Parse BDD labels into validated detections.
3. Run Qwen3-VL full-image grounding inference.
4. Compute class-threshold QC flags.
5. Persist run outputs and log to MLflow.
6. Surface the same package through Azure ML and Databricks wrappers.

Main modules:
- `src/qwen_auto_qc/config.py`: typed runtime config
- `src/qwen_auto_qc/dataset.py`: BDD detection extraction
- `src/qwen_auto_qc/inference.py`: grounding prompt + Qwen3-VL inference
- `src/qwen_auto_qc/scoring.py`: thresholding and QC decisions
- `src/qwen_auto_qc/results.py`: structured artifact writing
- `src/qwen_auto_qc/pipeline.py`: end-to-end orchestration
- `src/qwen_auto_qc/mlflow_tracking.py`: MLflow logging

## Local Setup
1. Install dependencies from `requirements.txt`.
2. Ensure the Qwen-VL runtime extras are available, including `qwen_vl_utils`.
3. Update `production/qwen_auto_qc/configs/local.yaml` if your dataset paths differ.
4. Run:

```bash
python production/qwen_auto_qc/run_cli.py run --config production/qwen_auto_qc/configs/local.yaml
```

## Output Contract
Each run writes:
- `run_config.json`
- `metrics.json`
- `run_summary.json`
- `all_samples.parquet` or CSV fallback
- `flagged_samples.parquet` or CSV fallback

`run_summary.json` contains:
- run id
- total sample count
- flagged sample count
- error rate
- mean latency
- thresholds
- artifact paths

## MLflow
- Enable MLflow in config before cloud runs.
- Standard tag: `algorithm=qwen_full_image_grounding`
- Log params, metrics, thresholds, and run artifacts.

## Azure ML
- Use `configs/azureml.yaml` for command jobs.
- The initial deployment shape is batch command execution, not an online endpoint.

## Azure DevOps
- PR validation runs lint, types, unit tests, and a smoke import.
- Main branch builds the package image and can trigger Azure ML batch execution.

## Databricks
- Use `databricks/auto_qc_job.py` to invoke the same package against batch data.
- The first version is file-based; promote to Delta-native ingestion after validation.

## Promotion Criteria
- Fixed benchmark slice is reproducible.
- CI passes.
- MLflow run artifacts are complete.
- Azure ML smoke job succeeds.

## Rollback
- Revert to the previous released package version and config bundle.
- Preserve prior run artifacts and MLflow metadata for auditability.

## Development Notes
- The package keeps experiment code untouched under `data_clean/confident_learning/`.
- Tests are deterministic and avoid external model dependencies by mocking the Qwen loader boundary.
- The local entrypoint is `run_cli.py`; the packaged entrypoint is `qwen-auto-qc`.
