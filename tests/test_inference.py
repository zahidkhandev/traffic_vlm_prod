import torch
from PIL import Image

from qwen_auto_qc.config import RunConfig
from qwen_auto_qc.inference import QwenGroundingInference


class _Tokenizer:
    def __call__(self, text, add_special_tokens=False):
        return type("TokenResult", (), {"input_ids": [len(text)]})


class _Processor:
    tokenizer = _Tokenizer()


class _Loaded:
    processor = _Processor()
    model = type("Model", (), {"device": "cpu"})()
    device = "cpu"


def test_build_grounding_prompt_contains_box_tokens():
    config = RunConfig()
    inferencer = QwenGroundingInference(config, loaded=_Loaded())
    prepared = inferencer.build_grounding_prompt(
        Image.new("RGB", (100, 100)), [10, 20, 30, 40]
    )
    assert "<|box_start|>" in prepared.prompt
    assert "trafficlight" in prepared.prompt


def test_parse_response_maps_aliases():
    config = RunConfig()
    inferencer = QwenGroundingInference(config, loaded=_Loaded())
    logits = torch.zeros(200)
    probs, label = inferencer.parse_response("trafficlight", logits)
    assert label == "traffic light"
    assert set(probs) == set(config.class_names)


def test_parse_response_falls_back_to_argmax():
    config = RunConfig()
    inferencer = QwenGroundingInference(config, loaded=_Loaded())
    logits = torch.zeros(200)
    logits[inferencer.class_first_token_ids[2]] = 10.0
    probs, label = inferencer.parse_response("unknown", logits)
    assert label == "car"
    assert probs["car"] == max(probs.values())
