import falcon
from falcon import testing
import json
from .utils import assert_dict, set_time_base

def test_get_all_bets(new_user, better_client):
	# type: (testing.TestClient) -> None
	response = better_client.simulate_get('/bet')
	assert response.status == falcon.HTTP_OK
	
	bets = json.loads(response.text)
	assert len(bets) == 64

	# check all bets are properly owned by caller
	assert len([bet for bet in bets if bet['better']['id'] == new_user['id']]) == 64
	# check all bets have no result
	assert len([bet for bet in bets if bet['result'] is not None]) == 0
	# check the number of bets for future matches
	assert len([bet for bet in bets if bet['match']['team1']['group'] == 'virtual']) == 16

def test_patch_bet_future_match(new_user, better_client, admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = better_client.simulate_get('/bet')
	bets = json.loads(response.text)
	# Take the first match in round 1
	id, match = [(bet['id'], bet['match']) for bet in bets if bet['match']['round'] == '1'][0]
	response = better_client.simulate_patch('/bet', body = json.dumps([{
		'id': id,
		'result': '2-1'
	}]))
	assert response.status == falcon.HTTP_OK
	
	# check returned result id and match
	bets = json.loads(response.text)
	assert len(bets) == 1
	bet = bets[0]
	del new_user['connection']
	expected = {
		'id': id,
		'better': new_user,
		'match': match,
		'result': '2-1'
	}
	assert_dict(expected, bet)
	
def test_patch_bet_past_match(admin_client, better_client):
	# type: (testing.TestClient) -> None
	# Requires time base change first (admin only)
	set_time_base(admin_client, '2018-06-30T14:30:00+00:00')
	response = better_client.simulate_get('/bet')
	bets = json.loads(response.text)
	# Take the first match in round 1
	id, match = [(bet['id'], bet['match']) for bet in bets if bet['match']['round'] == '1'][0]
	response = better_client.simulate_patch('/bet', body = json.dumps([{
		'id': id,
		'result': '2-1'
	}]))
	assert response.status == falcon.HTTP_FORBIDDEN

	response = admin_client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK

def test_patch_bet_unknown_match(better_client):
	# type: (testing.TestClient) -> None
	response = better_client.simulate_get('/bet')
	bets = json.loads(response.text)
	# Take the first match in 2nd phase
	id, match = [(bet['id'], bet['match']) for bet in bets if bet['match']['round'] == 'Round of 16'][0]
	response = better_client.simulate_patch('/bet', body = json.dumps([{
		'id': id,
		'result': '2-1'
	}]))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	
def test_patch_bet_bad_result(better_client, admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = better_client.simulate_get('/bet')
	bets = json.loads(response.text)
	# Take the first match in 1st phase
	id, match = [(bet['id'], bet['match']) for bet in bets if bet['match']['round'] == '1'][0]
	response = better_client.simulate_patch('/bet', body = json.dumps([{
		'id': id,
		'result': '2-X'
	}]))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	