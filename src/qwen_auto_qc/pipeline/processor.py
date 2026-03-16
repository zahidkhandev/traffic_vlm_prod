from __future__ import annotations

from pathlib import Path

from ..config import RunConfig
from ..dataset import BDDDatasetParser
from ..mlflow_tracking import log_run_to_mlflow
from ..results import create_run_dir, persist_run
from ..types import InferenceResult, RunSummary
from ..vlm.classifier import QwenGroundingInference
from .checkpoint import save_processed_images
from ..analysis.scoring import derive_thresholds, make_decisions


class AutoQCPipeline:
    def __init__(self, config: RunConfig, inferencer: QwenGroundingInference | None = None):
        self.config = config
        self.parser = BDDDatasetParser(config)
        self.inferencer = inferencer or QwenGroundingInference(config)

    def run(self) -> tuple[RunSummary, Path]:
        run_dir = create_run_dir(self.config.output_root)
        checkpoint_path = Path(self.config.checkpoint_root) / f"{run_dir.name}.json"

        samples = self.parser.iter_samples()
        results: list[InferenceResult] = []
        processed_image_ids: set[str] = set()

        for index, sample in enumerate(samples, start=1):
            result = self.inferencer.predict(sample)
            results.append(result)
            processed_image_ids.add(sample.image_id)

            if index % self.config.checkpoint_every == 0:
                save_processed_images(checkpoint_path, processed_image_ids)

        thresholds = self.config.thresholds or derive_thresholds(samples, results)
        decisions = make_decisions(samples, results, thresholds)
        summary = persist_run(self.config, decisions, thresholds, run_dir)
        log_run_to_mlflow(self.config, summary, run_dir)
        return summary, run_dir
