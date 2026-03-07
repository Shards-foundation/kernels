PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install install-dev lint format typecheck test test-cov security smoke qa ci clean

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e .
	$(PIP) install pytest pytest-cov ruff mypy bandit pip-audit pre-commit

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy kernels implementations

test:
	pytest

test-cov:
	pytest --cov=kernels --cov=implementations --cov-report=term-missing --cov-fail-under=80

security:
	bandit -r kernels implementations -q
	pip-audit

smoke:
	bash scripts/smoke.sh

qa:
	$(PYTHON) -m pip check
	$(PYTHON) -m build --sdist --wheel

ci: lint typecheck security test-cov smoke qa

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
