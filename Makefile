lint: ## Lint code
	flake8 src/ tests/ --count


format: ## Format code
	black src/ tests/


pytest: ## pytest
	python -m pytest tests


pytest-coverage: ##
	python -m pytest tests --doctest-modules --junitxml=junit/test-results.xml --cov=src --cov-report=xml --cov-report=html
	open htmlcov/index.html

install-requirements:
	pip install -r requirements.txt

install-poetry:
	pip install poetry==1.4.1
	poetry add `cat requirements.txt`
