from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
import base64
import falcon
from falcon import testing
from falcon.testing import helpers
import json
import pytest
from .utils import href, assert_dict, set_time_base, reset_time_base

from example4.app import api

@pytest.fixture
def client():
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

def test_get_time(client):
	response = client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert actual['delta'] == 0

	now = parse_date(actual['now'])
	delta = now - datetime.now(timezone.utc)
	assert -2 < delta.total_seconds() < +2

def test_patch_time_base(client):
	base = '2018-01-01T14:30:00+00:00'
	set_time_base(client, base)
	base = parse_date(base)
	delta = base - datetime.now(timezone.utc)

	response = client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert -2 < actual['delta'] - delta.total_seconds() < 2

	now = parse_date(actual['now'])
	delta = base - now
	assert -2 < delta.total_seconds() < +2

	response = client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK

def test_patch_time_delta(client):
	base = parse_date('2018-01-01T14:30:00+00:00')
	delta = (base - datetime.now(timezone.utc)).total_seconds()
	response = client.simulate_patch('/time', body = json.dumps({
		'delta': delta
	}))
	assert response.status == falcon.HTTP_OK

	response = client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert -2 < actual['delta'] - delta < 2

	now = parse_date(actual['now'])
	delta = base - now
	assert -2 < delta.total_seconds() < +2

	response = client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK

def test_list_teams(client):
	response = client.simulate_get('/team')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert len(actual) == 32
	expected = {
		'id': 1,
		'href': href('/team/1'),
		'name': 'Egypt',
		'group': 'Group A',
		'rank': None,
		'played': 0,
		'won': 0,
		'drawn': 0,
		'lost': 0,
		'goals_for': 0,
		'goals_against': 0,
		'goals_diff': 0,
		'points': 0,
	}
	assert actual[0] == expected
	expected = {
		'id': 32,
		'href': href('/team/32'),
		'name': 'Senegal',
		'group': 'Group H',
		'rank': None,
		'played': 0,
		'won': 0,
		'drawn': 0,
		'lost': 0,
		'goals_for': 0,
		'goals_against': 0,
		'goals_diff': 0,
		'points': 0,
	}
	assert actual[31] == expected
    
def test_get_team(client):
	response = client.simulate_get('/team/11')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'id': 11,
		'href': href('/team/11'),
		'name': 'France',
		'group': 'Group C',
		'rank': None,
		'played': 0,
		'won': 0,
		'drawn': 0,
		'lost': 0,
		'goals_for': 0,
		'goals_against': 0,
		'goals_diff': 0,
		'points': 0,
	}
	assert actual == expected

def test_list_venues(client):
	response = client.simulate_get('/venue')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert len(actual) == 12
	expected = {
		'href': href('/venue/1'),
		'id': 1,
		'name': 'Ekaterinburg Stadium',
	}
	assert actual[0] == expected
	expected = {
		'href': href('/venue/12'),
		'id': 12,
		'name': 'Volgograd Stadium',
	}
	assert actual[11] == expected
    
def test_get_venue(client):
	response = client.simulate_get('/venue/5')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/venue/5'),
		'id': 5,
		'name': 'Luzhniki Stadium, Moscow',
	}
	assert actual == expected

def test_list_matches(client):
	response = client.simulate_get('/match')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert len(actual) == 64

	expected = {
		'href': href('/match/1'),
		'round': '1',
		'matchtime': '2018-06-14T15:00:00+00:00',
		'group': 'Group A',
		'venue': {
			'name': 'Luzhniki Stadium, Moscow'
		},
		'team1': {
			'name': 'Russia'
		},
		'team2': {
			'name': 'Saudi Arabia'
		}
	}
	assert_dict(expected, actual[0])

	expected = {
		'href': href('/match/49'),
		'round': 'Round of 16',
		'matchtime': '2018-06-30T18:00:00+00:00',
		'group': '',
		'venue': {
			'name': 'Fisht Stadium, Sochi'
		},
		'team1': {
			'name': 'Winner Group A'
		},
		'team2': {
			'name': 'Runner-up Group B'
		}
	}
	assert_dict(expected, actual[48])
    
def test_get_match(client):
	response = client.simulate_get('/match/35')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-25T18:00:00+00:00',
		'group': 'Group B',
		'venue': {
			'href': href('/venue/11'),
			'name': 'Saransk Stadium'
		},
		'team1': {
			'href': href('/team/5'),
			'name': 'Iran'
		},
		'team2': {
			'href': href('/team/7'),
			'name': 'Portugal'
		}
	}
	assert_dict(expected, actual)

def test_patch_match_time(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-01T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'matchtime': '2018-06-26T18:00:00+00:00'
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-26T18:00:00+00:00',
		'group': 'Group B'
	}
	assert_dict(expected, actual)

	response = client.simulate_patch('/match/35', body = json.dumps({
		'matchtime': '2018-06-25T18:00:00+00:00'
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_venue(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-01T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 1
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-25T18:00:00+00:00',
		'group': 'Group B',
		'venue': {
			'href': href('/venue/1'),
			'name': 'Ekaterinburg Stadium'
		}
	}
	assert_dict(expected, actual)

	response = client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 11
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_unknown_venue(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-01T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 24
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'title': 'Integrity constraint error'
	}
	assert_dict(expected, actual)

def test_patch_match_teams(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-01T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 1,
		'team2_id': 2
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-25T18:00:00+00:00',
		'group': 'Group B',
		'team1': {
			'href': href('/team/1'),
			'name': 'Egypt'
		},
		'team2': {
			'href': href('/team/2'),
			'name': 'Russia'
		}
	}
	assert_dict(expected, actual)

	response = client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 5,
		'team2_id': 7
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_unknown_team(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-01T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 124
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'title': 'Integrity constraint error'
	}
	assert_dict(expected, actual)

def test_patch_match_result(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-26T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'result': '0-3'
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'result': '0-3',
		'group': 'Group B'
	}
	assert_dict(expected, actual)

	response = client.simulate_patch('/match/35', body = json.dumps({
		'result': None
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_incorrect_result(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-26T00:00:00+00:00')
	response = client.simulate_patch('/match/35', body = json.dumps({
		'result': '0-X'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'description': json.dumps({
			'result': ['result must comply to format "0-0"']
		})
	}
	assert_dict(expected, actual)

def test_patch_future_match_result(client):
	# type: (testing.TestClient) -> None
	set_time_base(client, '2018-06-26T00:00:00+00:00')
	response = client.simulate_patch('/match/64', body = json.dumps({
		'result': '0-1'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'description': 'This match has not been played yet, it is not allowed to set its result.'
	}
	assert_dict(expected, actual)

def test_patch_match_forbidden_field(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_patch('/match/35', body = json.dumps({
		'group': 'Group C'
	}))
	print(response.text)
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'description': json.dumps({
			"group": ["Unknown field"]
		})
	}
	assert_dict(expected, actual)

def test_list_users(client):
	response = client.simulate_get('/user')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert len(actual) == 1
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'email': 'jfpoilpret@gmail.com',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved',
	}
	assert_dict(expected, actual[0])
	#TODO check password is not present
    
def test_get_user_by_id(client):
	response = client.simulate_get('/user/1')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'email': 'jfpoilpret@gmail.com',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved',
	}
	assert_dict(expected, actual)

def test_get_user_by_login(client):
	response = client.simulate_get('/user/jfpoilpret@gmail.com')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'email': 'jfpoilpret@gmail.com',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, actual)

def test_get_user_by_bad_login(client):
	response = client.simulate_get('/user/jfp@jfp.org')
	assert response.status == falcon.HTTP_NOT_FOUND

def test_post_user(client):
	response = client.simulate_post('/user', body = json.dumps({
		'email': 'dummy@dummy.com',
		'password': 'dummy',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_CREATED
	
	user =  json.loads(response.text)
	expected = {
		'email': 'dummy@dummy.com',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved',
		'score': 0,
		'connection': None
	}
	assert_dict(expected, user)

	# check creation date
	creation = parse_date(user['creation'])
	delta = creation - datetime.now(timezone.utc)
	assert -2 < delta.total_seconds() < +2

	# delete user
	response = client.simulate_delete('/user/%d' % user['id'])
	assert response.status == falcon.HTTP_NO_CONTENT

def test_patch_user(client):
	response = client.simulate_patch('/user/jfpoilpret@gmail.com', body = json.dumps({
		'email': 'jfp@gmail.com',
		'password': 'jfpjfp',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK
	
	user =  json.loads(response.text)
	expected = {
		'email': 'jfp@gmail.com',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, user)

	response = client.simulate_patch('/user/jfp@gmail.com', body = json.dumps({
		'email': 'jfpoilpret@gmail.com',
		'password': 'jfp',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK
