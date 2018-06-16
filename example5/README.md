Python Falcon Example 5
=======================

Example5 includes a front-end (Vue.js, TypeScript, Bootstrap), Postgres support.

Preparation
-----------
Prepare a virtual environment for the project sample:

	cd example5
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install falcon
	pip3 install falcon-marshmallow
	pip3 install sqlalchemy
	pip3 install falcon-auth
	pip3 install pyyaml
	pip3 install gunicorn	# Web server engine used for testing and prod

Also install useful tools during project development:

	pip3 install ipython	# IDLE useful for checking API doc
	pip3 install httpie	# A better curl, useful for testing REST API
	pip3 install pytest	# Automated tests library
	pip3 install python-dateutil	# date parse utility used by unit tests
	pip3 install behave	# BDD test library


Develop fifth example
----------------------
Install Angular CLI

	> sudo npm install -g @angular/cli

Create application and add dependencies

	> ng new front-end
	> cd front-end
	> npm install bootstrap
	> npm install --save @ng-bootstrap/ng-bootstrap

Build and run front-end
	> npm start


Debug with Visual Studio Code
-----------------------------

Open `server.py` file and run Debug "Python: Current File".

