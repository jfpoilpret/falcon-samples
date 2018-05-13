Python Falcon Example 3
=======================

Example3 includes persistence through SQLAlchemy integration.
Since there is no proper Falcon-SQLAlchemy integration project, we have to roll our own, based on Falcon [middleware](http://falcon.readthedocs.io/en/stable/api/middleware.html) and SQLAlchemy [Sessions](https://docs.sqlalchemy.org/en/latest/orm/contextual.html#unitofwork-contextual).

Preparation
-----------
Prepare a virtual environment for the project sample:

	cd example2
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install falcon
	pip3 install falcon-marshmallow
	pip3 install sqlalchemy

Also install useful tools during project development:

	pip3 install ipython	# IDLE useful for checking API doc
	pip3 install gunicorn	# Web server engine useful for testing
	pip3 install httpie	# A better curl, useful for testing REST API
	pip3 install pytest	# Automated tests library

Develop third example
----------------------
Create new module from copy of example2 (without `.venv`, `__pycache__`...)



Debug with Visual Studio Code
-----------------------------

Open `server.py` file and run Debug "Python: Current File".

