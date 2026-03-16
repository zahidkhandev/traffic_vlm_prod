from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from .config import RunConfig, save_run_config
from .types import QCDecision, RunSummary


def create_run_dir(output_root: str) -> Path:
    run_id = datetime.now(UTC).strftime("run_%Y%m%d_%H%M%S")
    run_dir = Path(output_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _write_table(df: pd.DataFrame, target: Path) -> Path:
    try:
        df.to_parquet(target, index=False)
        return target
    except Exception:
        fallback = target.with_suffix(".csv")
        df.to_csv(fallback, index=False)
        return fallback


def persist_run(
    config: RunConfig,
    decisions: list[QCDecision],
    thresholds: dict[str, float],
    run_dir: Path,
) -> RunSummary:
    records = [decision.to_record() for decision in decisions]
    all_df = pd.DataFrame(records)
    flagged_df = all_df[all_df["is_error"] == True].copy()  # noqa: E712

    all_path = _write_table(all_df, run_dir / "all_samples.parquet")
    flagged_path = _write_table(flagged_df, run_dir / "flagged_samples.parquet")

    latencies = [decision.inference.latency_ms for decision in decisions]
    mean_latency = sum(latencies) / len(latencies) if latencies else 0.0

    summary = RunSummary(
        run_id=run_dir.name,
        total_samples=len(decisions),
        flagged_samples=len(flagged_df),
        error_rate=(len(flagged_df) / len(decisions)) if decisions else 0.0,
        mean_latency_ms=mean_latency,
        thresholds=thresholds,
        metrics={
            "total_samples": float(len(decisions)),
            "flagged_samples": float(len(flagged_df)),
            "error_rate": (len(flagged_df) / len(decisions)) if decisions else 0.0,
            "mean_latency_ms": mean_latency,
        },
        artifact_paths={
            "all_samples": str(all_path),
            "flagged_samples": str(flagged_path),
        },
    )

    save_run_config(config, run_dir / "run_config.json")
    (run_dir / "metrics.json").write_text(
        json.dumps(summary.metrics, indent=2), encoding="utf-8"
    )
    (run_dir / "run_summary.json").write_text(
        json.dumps(asdict(summary), indent=2), encoding="utf-8"
    )
    return summary
