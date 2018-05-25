Python Falcon Example 4
=======================

Example4 includes authentication and authorization, in addition to configuration options (target environments).

Preparation
-----------
Prepare a virtual environment for the project sample:

	cd example4
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install falcon
	pip3 install falcon-marshmallow
	pip3 install sqlalchemy
	pip3 install falcon-auth
	pip3 install pyyaml

Also install useful tools during project development:

	pip3 install ipython	# IDLE useful for checking API doc
	pip3 install gunicorn	# Web server engine useful for testing
	pip3 install httpie	# A better curl, useful for testing REST API
	pip3 install pytest	# Automated tests library

Develop fourth example
----------------------
Create new module from copy of example4 (without `.venv`, `__pycache__`...)



Debug with Visual Studio Code
-----------------------------

Open `server.py` file and run Debug "Python: Current File".

