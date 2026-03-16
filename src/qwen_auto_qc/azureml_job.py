from __future__ import annotations

from dataclasses import asdict, dataclass

from .config import RunConfig


@dataclass(slots=True)
class AzureMLJobSpec:
    display_name: str
    code: str
    command: str
    environment: str
    compute: str
    experiment_name: str
    inputs: dict[str, str]


def build_azureml_command_job(
    config: RunConfig,
    compute: str = "gpu-cluster",
    environment: str = "qwen-autoqc:latest",
) -> AzureMLJobSpec:
    return AzureMLJobSpec(
        display_name="qwen-auto-qc-batch",
        code="production/qwen_auto_qc",
        command="python run_cli.py run --config configs/azureml.yaml",
        environment=environment,
        compute=compute,
        experiment_name=config.mlflow.experiment_name,
        inputs={
            "images_path": config.images_path,
            "labels_path": config.labels_path,
            "model_path": config.model_path,
        },
    )


def azureml_job_as_dict(config: RunConfig) -> dict[str, object]:
    return asdict(build_azureml_command_job(config))
