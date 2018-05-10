Python Falcon Example 1
=======================

Preparation
-----------
Prepare a virtual environment for the project sample:

	mkdir example1
	cd example1
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install falcon

Also install useful tools during project development:

	pip3 install ipython	# IDLE useful for checking API doc
	pip3 install gunicorn	# Web server engine useful for testing
	pip3 install httpie	# A better curl, useful for testing
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

