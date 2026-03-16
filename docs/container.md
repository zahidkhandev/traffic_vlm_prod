# Container Guide

## Build
```bash
cd production/qwen_auto_qc
docker build -t qwen-auto-qc:local .
```

## Docker Run
Mount data and model paths that match the config inside the container.

Example:
```bash
docker run --rm ^
  -v <host-data-path>:/app/data ^
  -v <host-model-path>:/app/qwen-vl-4b ^
  qwen-auto-qc:local
```

If the model path differs in-container, update `configs/local.yaml` or pass a different config.

## Podman Build
```bash
cd production/qwen_auto_qc
podman build -f Containerfile -t qwen-auto-qc:local .
```

## Podman Run
```bash
podman run --rm \
  -v <host-data-path>:/app/data \
  -v <host-model-path>:/app/qwen-vl-4b \
  qwen-auto-qc:local
```

Both container files are local to this isolated project root:
- `Dockerfile`
- `Containerfile`
