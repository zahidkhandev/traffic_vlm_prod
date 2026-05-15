from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and prepare Azure ML pipeline inputs."
    )
    parser.add_argument("--images-path", required=True)
    parser.add_argument("--labels-path", required=True)
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    images_path = Path(args.images_path)
    labels_path = Path(args.labels_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not images_path.exists():
        raise FileNotFoundError(f"images path does not exist: {images_path}")
    if not labels_path.exists():
        raise FileNotFoundError(f"labels path does not exist: {labels_path}")

    label_files = sorted(labels_path.glob("*.json"))
    image_files = sorted(images_path.glob("*.jpg"))
    if not label_files:
        raise RuntimeError(f"no label files found in: {labels_path}")
    if not image_files:
        raise RuntimeError(f"no image files found in: {images_path}")

    payload = {
        "images_path": str(images_path),
        "labels_path": str(labels_path),
        "label_file_count": len(label_files),
        "image_file_count": len(image_files),
    }
    target = output_dir / "prepared_inputs.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
