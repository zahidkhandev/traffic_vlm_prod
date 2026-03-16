import pytest

from qwen_auto_qc.config import load_run_config


def test_default_config_requires_runtime_paths():
    with pytest.raises(ValueError, match="Missing required config values"):
        load_run_config(None)
