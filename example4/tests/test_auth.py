from uuid import uuid4
import falcon
from falcon import testing
from falcon.testing import helpers
import base64
import json
import pytest
from datetime import datetime

from example4.app import api

@pytest.fixture
def client():
    # type: () -> testing.TestClient
    return testing.TestClient(api)

def test_get_token_no_credentials(client):
	response = client.simulate_get('/token')
	assert response.status == falcon.HTTP_UNAUTHORIZED

def test_get_token_bad_login(client):
	token = base64.b64encode('dummy:xxx'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_UNAUTHORIZED


def test_get_token_bad_password(client):
	token = base64.b64encode('jfpoilpret:xxx'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_UNAUTHORIZED

def test_get_token_good_credentials(client):
	token = base64.b64encode('jfpoilpret:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert 'token' in actual
	assert actual['token']
	# check expiry date
	assert 'expiry' in actual
	# remove timezone
	expiry = actual['expiry'][:-6]
	# remove microseconds
	if expiry.index('.') > 0:
		expiry = expiry[:expiry.index('.')]
	expiry = datetime.strptime(expiry, '%Y-%m-%dT%H:%M:%S')
	delta = expiry - datetime.now()
	assert 86350 < delta.total_seconds() < 86450

def test_other_resource_basic_credentials(client):
	token = base64.b64encode('jfpoilpret:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/venue/5', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_UNAUTHORIZED

def test_other_resource_no_token(client):
	response = client.simulate_get('/venue/5')
	assert response.status == falcon.HTTP_UNAUTHORIZED

def test_other_resource_bad_token(client):
	token = uuid4()
	response = client.simulate_get('/venue/5', headers = {
		'Authorization': 'Token %s' % token
	})
	assert response.status == falcon.HTTP_UNAUTHORIZED

def test_other_resource_correct_token(client):
	token = base64.b64encode('jfpoilpret:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	token = actual['token']
	response = client.simulate_get('/venue/5', headers = {
		'Authorization': 'Token %s' % token
	})
	assert response.status == falcon.HTTP_OK
