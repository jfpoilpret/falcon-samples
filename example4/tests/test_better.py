from datetime import datetime
import base64
import falcon
from falcon import testing
from falcon.testing import helpers
import json
import pytest
from .utils import href, json_to_datetime, assert_dict

from example4.app import api

#TODO Do we need to delete new user?
@pytest.fixture
def client():
	# type: () -> testing.TestClient
	client = testing.TestClient(api)
	# authenticate admin
	token = base64.b64encode('jfpoilpret:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK
	token = json.loads(response.text)['token']
	# create new user for the tests
	response = client.simulate_post('/user', headers = {
		'Authorization': 'Token %s' % token
	}, body = json.dumps({
		'login': 'better',
		'password': 'better',
		'status': 'approved',
		'fullname': 'John Doe',
		'email': 'john@doe.com'
	}))
	assert response.status == falcon.HTTP_CREATED

	# authenticate new user
	token = base64.b64encode('better:better'.encode('utf-8')).decode('utf-8', 'ignore')
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

def test_get_all_bets(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_get('/bet')
	assert response.status == falcon.HTTP_OK
	
	bets = json.loads(response.text)
	assert len(bets) == 64

	# check all bets have no result
	assert len([bet for bet in bets if bet['result'] is not None]) == 0
	# check the number of bets for future matches
	assert len([bet for bet in bets if bet['match']['team1'] is None]) == 16

def test_patch_bet_future_match(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_get('/bet')
	bets = json.loads(response.text)
	# Take the first match in round 1
	id, match = [(bet['id'], bet['match']) for bet in bets if bet['match']['round'] == '1'][0]
	response = client.simulate_patch('/bet', body = json.dumps([{
		'id': id,
		'result': '2-1'
	}]))
	assert response.status == falcon.HTTP_OK
	#TODO check returned result id and match
	
def test_patch_bet_past_match(client):
	# type: (testing.TestClient) -> None
	# Requires time base change first (admin only)
	pass
	
def test_patch_bet_unknown_match(client):
	# type: (testing.TestClient) -> None
	pass
	