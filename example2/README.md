Python Falcon Example 2
=======================

This example adds JSON validation through Marshmallow integration to Falcon. It also implements extra simple persistence to a JSON file.

Preparation
-----------
Prepare a virtual environment for the project sample:

	cd example2
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install falcon
	pip3 install falcon-marshmallow

Also install useful tools during project development:

	pip3 install ipython	# IDLE useful for checking API doc
	pip3 install gunicorn	# Web server engine useful for testing
	pip3 install httpie	# A better curl, useful for testing REST API
	pip3 install pytest	# Automated tests library

Develop second example
----------------------
Create new module from copy of first example1 (without `.venv`, `__pycache__`).



Debug with Visual Studio Code
-----------------------------

Open `server.py` file and run Debug "Python: Current File".
