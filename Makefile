.PHONY: help
.DEFAULT_GOAL := help

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  install   Install requirements"
	@echo "  lock      Lock project dependencies"
	@echo "  update    Update project dependencies"
	@echo "  format    Run code formatters"
	@echo "  lint      Run code linters"

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade poetry
	poetry install --no-root

lock:
	poetry lock

update:
	poetry update

format:
	poetry run ruff format src tests
	poetry run ruff check  src tests --fix

lint:
	poetry run ruff format src tests --check
	poetry run ruff check  src tests
	poetry run mypy src tests