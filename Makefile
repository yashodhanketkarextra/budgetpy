.PHONY: dev prod test coverage setup deps-install deps-lock-file docker-build docker-run

dev:
	@PY_ENV=dev python server.py -m dev

prod:
	@PY_ENV=prod python server.py -m prod

test:
	@PYTHONPATH=src PY_ENV=test pytest

coverage:
	@PYTHONPATH=src PY_ENV=test pytest --cov=src --cov-report=html

deps-install:
	@pip install -r requirements.txt

deps-lock-file:
	@pip freeze > requirements.txt

docker-build:
	@docker-compose build

docker-run:
	@docker-compose up -d

setup:
	@if [ ! -d "./venv/" ]; then \
		python -m venv venv; \
	fi
	@./venv/bin/pip install -r requirements.txt
	@echo "Use 'source ./venv/bin/activate' to get started"

