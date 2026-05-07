dev:
	@PY_ENV=dev python server.py -m dev

prod:
	@PY_ENV=prod python server.py -m prod

test:
	@PYTHONPATH=src PY_ENV=test pytest

deps-install:
	@pip install -r requirements.txt

deps-lock-file:
	@pip freeze > requirements.txt
