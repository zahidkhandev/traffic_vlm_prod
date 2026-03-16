from __future__ import annotations

from collections import defaultdict

from ..types import DetectionSample, InferenceResult, QCDecision


def compute_margin(pred_probs: dict[str, float], given_label: str) -> tuple[float, float]:
    self_confidence = float(pred_probs.get(given_label, 0.0))
    ordered = sorted(pred_probs.values(), reverse=True)
    top_conf = ordered[0] if ordered else 0.0
    margin = max(top_conf - self_confidence, 0.0)
    normalized = margin / top_conf if top_conf > 0 else 0.0
    return self_confidence, normalized


def derive_thresholds(
    samples: list[DetectionSample], results: list[InferenceResult]
) -> dict[str, float]:
    by_class: dict[str, list[float]] = defaultdict(list)
    for sample, result in zip(samples, results):
        by_class[sample.given_label].append(
            float(result.pred_probs.get(sample.given_label, 0.0))
        )

    thresholds: dict[str, float] = {}
    for label, values in by_class.items():
        thresholds[label] = min(values) if values else 0.0
    return thresholds


def make_decisions(
    samples: list[DetectionSample],
    results: list[InferenceResult],
    thresholds: dict[str, float],
) -> list[QCDecision]:
    decisions: list[QCDecision] = []
    for sample, result in zip(samples, results):
        self_confidence, normalized_margin = compute_margin(
            result.pred_probs, sample.given_label
        )
        threshold = thresholds.get(sample.given_label, 0.0)
        is_error = (
            self_confidence <= threshold
            and result.predicted_label != sample.given_label
        )
        decisions.append(
            QCDecision(
                sample=sample,
                inference=result,
                self_confidence=self_confidence,
                margin=result.predicted_confidence - self_confidence,
                normalized_margin=normalized_margin,
                is_error=is_error,
                reason_code="below_class_threshold" if is_error else "accepted",
            )
        )
    return decisions
