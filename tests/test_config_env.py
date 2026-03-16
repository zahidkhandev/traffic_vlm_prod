import os
import shutil
from pathlib import Path

from qwen_auto_qc.config import load_run_config


def test_load_run_config_expands_environment_variables():
    temp_root = Path("test_output/config_env")
    if temp_root.exists():
        shutil.rmtree(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)
    config_file = temp_root / "config.yaml"
    config_file.write_text(
        "images_path: ${AUTOQC_IMAGES_PATH}\nlabels_path: ${AUTOQC_LABELS_PATH}\n",
        encoding="utf-8",
    )
    os.environ["AUTOQC_IMAGES_PATH"] = "images/path"
    os.environ["AUTOQC_LABELS_PATH"] = "labels/path"
    config = load_run_config(config_file)
    assert config.images_path == "images/path"
    assert config.labels_path == "labels/path"
