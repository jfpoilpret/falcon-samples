from datetime import datetime
import base64
import logging
import falcon
from falcon import testing
from falcon.testing import helpers
import json
import pytest

logger = logging.getLogger(__name__)

def href(path):
    return 'http://' + helpers.DEFAULT_HOST + path

def json_to_datetime(dt):
	dt = dt[:-6]
	if dt.index('.') > 0:
		dt = dt[:dt.index('.')]
	return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')

def assert_dict(expected, actual):
	for key, value in expected.items():
		logger.debug('assert_dict() %s %s %s', key, str(value), str(actual[key]))
		if isinstance(value, dict):
			assert_dict(value, actual[key])
		else:
			assert value == actual[key]

