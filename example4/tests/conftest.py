import base64
import falcon
from falcon import testing
from falcon.testing import helpers
import json
import pytest
from .utils import set_time_base, reset_time_base

from example4.app import api

@pytest.fixture
def client():
    # type: () -> testing.TestClient
    return testing.TestClient(api)

@pytest.fixture
def admin_client():
	# type: () -> testing.TestClient
	client = testing.TestClient(api)
	# authenticate admin
	token = base64.b64encode('jfpoilpret@gmail.com:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK
	token = json.loads(response.text)['token']
	client._default_headers = {
		'Authorization': 'Token %s' % token
	}
	yield client
	reset_time_base(client)

@pytest.fixture
def new_user(admin_client):
	# create new user for the tests
	response = admin_client.simulate_post('/user', body = json.dumps({
		'email': 'john@doe.com',
		'password': 'john@doe.com',
		'status': 'approved',
		'fullname': 'John Doe',
	}))
	assert response.status == falcon.HTTP_CREATED
	user = json.loads(response.text)
	yield user
	# delete user before next test
	response = admin_client.simulate_delete('/user/%d' % user['id'])

@pytest.fixture
def better_client(new_user):
	# type: () -> testing.TestClient
	client = testing.TestClient(api)
	# authenticate new user
	token = '%s:%s' % (new_user['email'], new_user['email'])
	token = base64.b64encode(token.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK
	token = json.loads(response.text)['token']
	client._default_headers = {
		'Authorization': 'Token %s' % token
	}
	assert response.status == falcon.HTTP_OK
	return client
