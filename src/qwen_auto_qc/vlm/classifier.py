from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import torch
from PIL import Image

from ..config import RunConfig
from ..model_loader import LoadedModel, load_qwen_model
from ..types import DetectionSample, InferenceResult

CLASS_TOKEN_ALIASES = {
    "traffic light": "trafficlight",
    "traffic sign": "trafficsign",
}
CLASS_ALIAS_REVERSE = {value: key for key, value in CLASS_TOKEN_ALIASES.items()}


@dataclass(slots=True)
class PreparedPrompt:
    image: Image.Image
    prompt: str


class QwenGroundingInference:
    def __init__(self, config: RunConfig, loaded: LoadedModel | None = None):
        self.config = config
        self.loaded = loaded or load_qwen_model(config.model_path, config.device)
        self.processor = self.loaded.processor
        self.model = self.loaded.model
        self.class_names = config.class_names
        self.prompt_names = [CLASS_TOKEN_ALIASES.get(name, name) for name in self.class_names]
        self.class_first_token_ids = [
            self.processor.tokenizer(name, add_special_tokens=False).input_ids[0]
            for name in self.prompt_names
        ]

    def build_grounding_prompt(
        self, full_img: Image.Image, box: list[int]
    ) -> PreparedPrompt:
        x1, y1, x2, y2 = box
        width, height = full_img.size
        norm_x1 = int((x1 / width) * 1000)
        norm_y1 = int((y1 / height) * 1000)
        norm_x2 = int((x2 / width) * 1000)
        norm_y2 = int((y2 / height) * 1000)
        class_names_str = ", ".join(self.prompt_names)
        prompt = (
            f"<|box_start|>({norm_x1},{norm_y1}),({norm_x2},{norm_y2})<|box_end|>\n"
            f"What object is inside this box region? Choose exactly ONE from: {class_names_str}.\n\n"
            f"Reply with ONLY the single word (no explanation)."
        )
        return PreparedPrompt(image=full_img, prompt=prompt)

    def parse_response(
        self, response_text: str, first_token_logits: torch.Tensor
    ) -> tuple[dict[str, float], str]:
        response_lower = response_text.lower().strip()
        parsed_class = None

        for alias, original in CLASS_ALIAS_REVERSE.items():
            if alias in response_lower:
                parsed_class = original
                break

        if parsed_class is None:
            for cls in self.class_names:
                if cls in response_lower:
                    parsed_class = cls
                    break

        class_logits = []
        for token_id in self.class_first_token_ids:
            class_logits.append(
                float(first_token_logits[token_id])
                if token_id < len(first_token_logits)
                else 0.0
            )

        probs_array = torch.nn.functional.softmax(
            torch.tensor(class_logits, dtype=torch.float32), dim=0
        ).cpu().numpy()
        probs = {cls: float(prob) for cls, prob in zip(self.class_names, probs_array)}

        if parsed_class is None:
            parsed_class = self.class_names[int(np.argmax(probs_array))]

        return probs, parsed_class

    def predict(self, sample: DetectionSample) -> InferenceResult:
        try:
            from qwen_vl_utils import process_vision_info
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "qwen_vl_utils is required for Qwen-VL image preprocessing."
            ) from exc

        full_img = Image.open(sample.image_path).convert("RGB")
        prepared = self.build_grounding_prompt(full_img, sample.box)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": prepared.image},
                    {"type": "text", "text": prepared.prompt},
                ],
            }
        ]
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        vision_outputs = process_vision_info(messages)
        image_inputs = vision_outputs[0]
        video_inputs = vision_outputs[1] if len(vision_outputs) > 1 else None
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = {
            key: value.to(self.model.device) if isinstance(value, torch.Tensor) else value
            for key, value in inputs.items()
        }

        started = time.perf_counter()
        with torch.no_grad():
            outputs = self.model(
                input_ids=inputs.get("input_ids"),
                attention_mask=inputs.get("attention_mask"),
                pixel_values=inputs.get("pixel_values"),
                image_grid_thw=inputs.get("image_grid_thw"),
                output_hidden_states=True,
            )
            embedding = outputs.hidden_states[-1].mean(dim=1).cpu().numpy()[0].tolist()

            generated = self.model.generate(
                input_ids=inputs.get("input_ids"),
                attention_mask=inputs.get("attention_mask"),
                pixel_values=inputs.get("pixel_values"),
                image_grid_thw=inputs.get("image_grid_thw"),
                max_new_tokens=5,
                do_sample=False,
                temperature=1.0,
                pad_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True,
                output_scores=True,
                return_dict_in_generate=True,
            )
        latency_ms = (time.perf_counter() - started) * 1000.0

        response = self.processor.batch_decode(
            generated.sequences, skip_special_tokens=True
        )[0]
        response_text = response.split("assistant")[-1].strip()
        first_token_logits = generated.scores[0][0]
        pred_probs, predicted_label = self.parse_response(
            response_text, first_token_logits
        )

        return InferenceResult(
            predicted_label=predicted_label,
            predicted_label_idx=self.class_names.index(predicted_label),
            predicted_confidence=pred_probs[predicted_label],
            pred_probs=pred_probs,
            embedding=embedding,
            raw_response=response_text,
            latency_ms=latency_ms,
        )
