from __future__ import annotations

import argparse
import json
from pathlib import Path

from qwen_auto_qc.config import load_run_config, validate_run_config
from qwen_auto_qc.pipeline.processor import AutoQCPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run AutoQC inference stage from prepared pipeline inputs."
    )
    parser.add_argument("--config", default="configs/azureml.yaml")
    parser.add_argument("--prepared-inputs", required=True)
    parser.add_argument("--model-path")
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prepared_inputs = Path(args.prepared_inputs)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = json.loads(prepared_inputs.read_text(encoding="utf-8"))
    config = load_run_config(args.config)
    config = config.copy_with(
        images_path=payload["images_path"],
        labels_path=payload["labels_path"],
        output_root=str(output_dir),
        checkpoint_root=str(output_dir / "checkpoints"),
        model_path=args.model_path or config.model_path,
    )
    config = validate_run_config(config)

    summary, run_dir = AutoQCPipeline(config).run()
    stage_summary = {
        "run_dir": str(run_dir),
        "run_id": summary.run_id,
        "metrics": summary.metrics,
        "artifact_paths": summary.artifact_paths,
    }
    (output_dir / "inference_summary.json").write_text(
        json.dumps(stage_summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(stage_summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
