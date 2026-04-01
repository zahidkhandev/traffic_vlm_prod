from __future__ import annotations

import json
from pathlib import Path

from .config import RunConfig
from .types import RunSummary


def log_run_to_mlflow(config: RunConfig, summary: RunSummary, run_dir: Path) -> None:
    if not config.mlflow.enabled:
        return

    try:
        import mlflow
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("MLflow logging requested but mlflow is not installed.") from exc

    if config.mlflow.tracking_uri:
        mlflow.set_tracking_uri(config.mlflow.tracking_uri)
    mlflow.set_experiment(config.mlflow.experiment_name)

    with mlflow.start_run(run_name=config.mlflow.run_name or summary.run_id):
        mlflow.set_tags(config.mlflow.tags)
        mlflow.log_params(
            {
                "model_path": config.model_path,
                "images_path": config.images_path,
                "labels_path": config.labels_path,
                "use_grounding": config.use_grounding,
                "max_samples": config.max_samples,
            }
        )
        mlflow.log_metrics(summary.metrics)
        thresholds_path = run_dir / "thresholds.json"
        thresholds_path.write_text(
            json.dumps(summary.thresholds, indent=2), encoding="utf-8"
        )
        mlflow.log_artifact(str(thresholds_path), artifact_path="config")
        for name, artifact in summary.artifact_paths.items():
            artifact_path = Path(artifact)
            if artifact_path.is_dir():
                mlflow.log_artifacts(str(artifact_path), artifact_path=name)
            elif artifact_path.exists():
                mlflow.log_artifact(str(artifact_path), artifact_path=name)
        mlflow.log_artifacts(str(run_dir), artifact_path="run_bundle")
