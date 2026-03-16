# Config Reference

This project mainly uses `configs/local.yaml`.

## Main config fields

### `model_path`
Required at runtime.
Pass through env var or CLI.
Path or model id for Qwen.

Example:
```yaml
model_path: models/qwen-vl-4b
```

### `images_path`
Required at runtime.
Pass through env var or CLI.
Path to images.

Use a relative path inside this project.

Example:
```yaml
images_path: data/raw/mini/images/test
```

### `labels_path`
Required at runtime.
Pass through env var or CLI.
Path to labels.

Use a relative path inside this project.

Example:
```yaml
labels_path: data/raw/mini/labels/test
```

### `output_root`
Where run outputs are written.

Example:
```yaml
output_root: runs
```

### `checkpoint_root`
Where checkpoints are written.

Example:
```yaml
checkpoint_root: checkpoints
```

### `device`
Usually:
- `auto`
- `cpu`
- `cuda`

### `max_samples`
Use this for smoke tests first.

Example:
```yaml
max_samples: 2
```

### `checkpoint_every`
Save progress after this many samples.

### `min_box_size`
Boxes smaller than this are ignored.

### `use_grounding`
Current production path should stay `true`.

## MLflow block

Example:
```yaml
mlflow:
  enabled: true
  tracking_uri: ${MLFLOW_TRACKING_URI}
  experiment_name: qwen_auto_qc
  tags:
    algorithm: qwen_full_image_grounding
    platform: local
```

## Environment variables

Defined in `.env.example`:

```env
AUTOQC_MODEL_PATH=models/qwen-vl-4b
AUTOQC_IMAGES_PATH=data/raw/mini/images/test
AUTOQC_LABELS_PATH=data/raw/mini/labels/test
MLFLOW_TRACKING_URI=file:./mlruns
```

## Recommended local smoke config

For first run:
```yaml
max_samples: 1
mlflow:
  enabled: false
```

After that:
```yaml
max_samples: 2
mlflow:
  enabled: true
```
