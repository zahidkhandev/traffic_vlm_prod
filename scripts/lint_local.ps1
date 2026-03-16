. .\.venv\Scripts\Activate.ps1
ruff check src tests
ruff format --check src tests
