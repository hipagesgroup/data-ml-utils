lint: ## Lint code
	flake8 hip_data_ml_utils/ tests/ --count


format: ## Format code
	black hip_data_ml_utils/ tests/


pytest: ## pytest
	python -m pytest tests

venv:
	python3 -m venv venv
	. venv/bin/activate

pytest-coverage: ##
	python -m pytest tests --doctest-modules --junitxml=junit/test-results.xml --cov=src --cov-report=xml --cov-report=html
	open htmlcov/index.html

install-requirements:
	pip install -r requirements.txt

install-poetry:
	pip install poetry==1.4.1
	poetry update
	poetry install

precommit-all:
	pre-commit run --all-files
