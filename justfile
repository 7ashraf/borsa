default:
    @just --list

# Start dev server with hot reload
dev:
    uv run uvicorn borsa.main:app --reload --host 0.0.0.0 --port 8000

# Run the full test suite
test:
    uv run pytest -v

# Run tests with coverage
test-cov:
    uv run pytest --cov=borsa --cov-report=term-missing -v

# Lint with ruff
lint:
    uv run ruff check src tests

# Format with ruff
fmt:
    uv run ruff format src tests

# Type-check with mypy
typecheck:
    uv run mypy src

# Run all checks (CI equivalent)
check: lint typecheck test

# Build docker image
build:
    docker build -t borsa:local .

# Run via docker compose
up:
    docker compose up --build

# Install dev dependencies
install:
    uv sync --extra dev

# Install pre-commit hooks
hooks:
    uv run pre-commit install
