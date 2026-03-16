from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(slots=True)
class LoadedModel:
    processor: object
    model: object
    device: str


def resolve_torch_device(requested: str) -> tuple[str, torch.dtype]:
    if requested == "auto":
        if torch.cuda.is_available():
            return "cuda", torch.float16
        return "cpu", torch.float32
    if requested == "cuda" and not torch.cuda.is_available():
        return "cpu", torch.float32
    return requested, torch.float16 if requested == "cuda" else torch.float32


def load_qwen_model(model_path: str, device: str = "auto") -> LoadedModel:
    try:
        from transformers import AutoProcessor, Qwen3VLForConditionalGeneration
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("transformers with Qwen3-VL support is required.") from exc

    resolved_device, torch_dtype = resolve_torch_device(device)
    processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        model_path,
        torch_dtype=torch_dtype,
        device_map=resolved_device,
        trust_remote_code=True,
    )
    model.eval()
    return LoadedModel(processor=processor, model=model, device=resolved_device)
