Python Falcon Example 1
=======================

This first example simply demonstrates a simple REST API with Falcon, without validation, authentication or persistence.
The purpose is to learn Falcon step by step.
The example also demonstrates unit tests for Falcon REST resources.
Finally, this shows how to easily run a server (with Gunicorn) and test it live, with curl or httpie.

Preparation
-----------
Prepare a virtual environment for the project sample:

	cd example1
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install falcon

Also install useful tools during project development:

	pip3 install ipython	# IDLE useful for checking API doc
	pip3 install gunicorn	# Web server engine useful for testing
	pip3 install httpie	# A better curl, useful for testing REST API
	pip3 install pytest	# Automated tests library

Develop first example
---------------------
Create a main module (same name as application, why is that mandatory? I don't know):

	mkdir example1
	
Create an empty `__init__.py` to make it a python module.

Create the main application file `app.py`:

	import falcon

	api = application = falcon.API()

Now run the server with gunicorn:

	gunicorn --reload example1.app

Run unit tests:

	pytest tests

Debug with Visual Studio Code
-----------------------------

Open `server.py` file and run Debug "Python: Current File".
