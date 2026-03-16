from __future__ import annotations

from pathlib import Path


def save_placeholder_plot(output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("Visualization placeholder", encoding="utf-8")
