from qwen_auto_qc.config import RunConfig, load_run_config


def test_default_config_thresholds():
    config = load_run_config(None)
    assert isinstance(config, RunConfig)
    assert "car" in config.thresholds
