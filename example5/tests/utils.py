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

def assert_dict(expected, actual):
	for key, value in expected.items():
		logger.debug('assert_dict() %s %s %s', key, str(value), str(actual[key]))
		if isinstance(value, dict):
			assert_dict(value, actual[key])
		else:
			assert value == actual[key]

def set_time_base(client, base):
	# type: (testing.TestClient, str) -> None
	response = client.simulate_patch('/time', body = json.dumps({
		'now': base
	}))
	assert response.status == falcon.HTTP_OK

def reset_time_base(client):
	# type: (testing.TestClient, str) -> None
	response = client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK
