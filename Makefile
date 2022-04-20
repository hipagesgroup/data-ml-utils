lint: ## Lint code
	flake8 src/ tests/ --count


format: ## Format code
	black src/ tests/


pytest: ## pytest
	python -m pytest tests


pytest-coverage: ##
	python -m pytest tests --doctest-modules --junitxml=junit/test-results.xml --cov=src --cov-report=xml --cov-report=html
	open htmlcov/index.html

local-docker-build-image-dev: ##
	aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 251259879778.dkr.ecr.ap-southeast-2.amazonaws.com
	docker build -t 251259879778.dkr.ecr.ap-southeast-2.amazonaws.com/dummy:dev .
	docker push 251259879778.dkr.ecr.ap-southeast-2.amazonaws.com/dummy:dev

local-docker-build-image-prod: ##
	aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 251259879778.dkr.ecr.ap-southeast-2.amazonaws.com
	docker build -t 251259879778.dkr.ecr.ap-southeast-2.amazonaws.com/dummy:prod .
	docker push 251259879778.dkr.ecr.ap-southeast-2.amazonaws.com/dummy:prod

install-requirements:
	pip install -r requirements.txt

install-poetry:
	pip install poetry==1.1.11
	poetry add `cat requirements.txt`