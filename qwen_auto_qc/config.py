from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from dataclasses import replace
from pathlib import Path
from typing import Any

from .types import OBJECT_CLASSES
from .vlm.prompt_modes import validate_inference_mode

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


@dataclass(slots=True)
class MLflowConfig:
    enabled: bool = False
    tracking_uri: str | None = None
    experiment_name: str = "qwen_auto_qc"
    run_name: str | None = None
    tags: dict[str, str] = field(
        default_factory=lambda: {"algorithm": "qwen_full_image_grounding"}
    )


@dataclass(slots=True)
class RunConfig:
    model_path: str = "qwen-vl-4b"
    images_path: str = "data/raw/images/test"
    labels_path: str = "data/raw/labels/test"
    output_root: str = "runs"
    checkpoint_root: str = "checkpoints"
    device: str = "auto"
    torch_dtype: str = "auto"
    max_samples: int | None = None
    checkpoint_every: int = 10
    min_box_size: int = 10
    debug: bool = False
    save_debug_images: bool = False
    use_grounding: bool = True
    inference_mode: str = "without_red_rectangle"
    experiment_modes: list[str] = field(default_factory=list)
    class_names: list[str] = field(default_factory=lambda: OBJECT_CLASSES.copy())
    thresholds: dict[str, float] = field(default_factory=dict)
    benchmark_warmup: int = 1
    benchmark_steps: int = 10
    mlflow: MLflowConfig = field(default_factory=MLflowConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def copy_with(self, **changes: Any) -> "RunConfig":
        return replace(self, **changes)


_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


def _expand_env_value(value: Any) -> Any:
    if isinstance(value, str):
        return _ENV_PATTERN.sub(lambda match: os.environ.get(match.group(1), match.group(0)), value)
    if isinstance(value, list):
        return [_expand_env_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _expand_env_value(item) for key, item in value.items()}
    return value


def _coerce_config(data: dict[str, Any]) -> RunConfig:
    data = _expand_env_value(data)
    mlflow_data = data.pop("mlflow", {})
    config = RunConfig(**data)
    config.inference_mode = validate_inference_mode(config.inference_mode)
    config.experiment_modes = [
        validate_inference_mode(mode) for mode in config.experiment_modes
    ]
    config.mlflow = MLflowConfig(**mlflow_data)
    if not config.thresholds:
        config.thresholds = {name: 0.0 for name in config.class_names}
    return config


def load_run_config(config_path: str | Path | None = None) -> RunConfig:
    if config_path is None:
        return _coerce_config({})

    path = Path(config_path)
    text = path.read_text(encoding="utf-8")

    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML is required to load YAML config files.")
        data = yaml.safe_load(text) or {}
    elif path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        raise ValueError(f"Unsupported config format: {path.suffix}")

    return _coerce_config(data)


def save_run_config(config: RunConfig, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
