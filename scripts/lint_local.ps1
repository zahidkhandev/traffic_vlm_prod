. .\.venv\Scripts\Activate.ps1
ruff check qwen_auto_qc tests
ruff format --check qwen_auto_qc tests
