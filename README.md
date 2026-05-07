Budget Tracker App
==================

Simple budget tracker backend for personal finance (backend only).

Tech stack
----------

-	[X] FastAPI (Integratd)
-	[X] JWT Authentication
-	[X] Docker/docker-compose (Partially integratd)
-	[ ] DB (planned ORM free)
	-	[ ] SQLite during dev phase
	-	[ ] PostgreSQL for prod
-	[ ] Deployment
	-	[ ] Managed Terraform
	-	[ ] AWS lambda
	-	[ ] AWS Cloudfront

### Installation

1.	Create a virtual environment

	```sh
	$ python -m venv venv
	```

2.	Install dependencies within the virtual environment

	```sh
	$ source ./venv/bin/activate
	(venv)$ pip install -r requirements.txt
	```

3.	Run the server

	```sh
	(venv)$ PY_ENV=dev python server.py -m dev # dev mode
	(venv)$ PY_ENV=prod python server.py -m prod # prod mode
	```

-	Or if you have make installed

	```sh
	# setup VE and dependencies
	$ make setup
	$ source ./venv/bin/activate

	# start server
	(venv)$ make dev # dev mode
	(venv)$ make prod # prod mode
	```

### License

This project is licensed under the [GNU GPLv3](./LICENSE). See the [license](./LICENSE) for more details.
