from datetime import datetime
import base64
import falcon
from falcon import testing
from falcon.testing import helpers
import json
import pytest

from example4.app import api

def href(path):
    return 'http://' + helpers.DEFAULT_HOST + path

def json_to_datetime(dt):
	dt = dt[:-6]
	if dt.index('.') > 0:
		dt = dt[:dt.index('.')]
	return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')

@pytest.fixture
def client():
	# type: () -> testing.TestClient
	client = testing.TestClient(api)
	# authenticate admin
	token = base64.b64encode('jfpoilpret:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	token = json.loads(response.text)['token']
	client._default_headers = {
		'Authorization': 'Token %s' % token
	}
	return client

def assert_dict(expected, actual):
	for key, value in expected.items():
		print("assert_dict() %s %s" % (key, str(value)))
		if isinstance(value, dict):
			assert_dict(value, actual[key])
		else:
			assert value == actual[key]

def test_get_time(client):
	response = client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert actual['delta'] == 0

	now = json_to_datetime(actual['now'])
	delta = now - datetime.now()
	assert -2 < delta.total_seconds() < +2

def test_patch_time_base(client):
	base = '2018-01-01T14:30:00'
	response = client.simulate_patch('/time', body = json.dumps({
		'now': base
	}))
	base = datetime.strptime(base, '%Y-%m-%dT%H:%M:%S')
	delta = base - datetime.now()
	assert response.status == falcon.HTTP_OK

	response = client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert -2 < actual['delta'] - delta.total_seconds() < 2

	now = json_to_datetime(actual['now'])
	delta = base - now
	assert -2 < delta.total_seconds() < +2

	response = client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK

def test_patch_time_delta(client):
	base = datetime.strptime('2018-01-01T14:30:00', '%Y-%m-%dT%H:%M:%S')
	delta = (base - datetime.now()).total_seconds()
	response = client.simulate_patch('/time', body = json.dumps({
		'delta': delta
	}))
	assert response.status == falcon.HTTP_OK

	response = client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert -2 < actual['delta'] - delta < 2

	now = json_to_datetime(actual['now'])
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
		'group': 'Group A'
	}
	assert actual[0] == expected
	expected = {
		'id': 32,
		'href': href('/team/32'),
		'name': 'Senegal',
		'group': 'Group H'
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
		'group': 'Group C'
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
		'matchtime': '2018-06-14T18:00:00+00:00',
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
		'matchtime': '2018-06-30T21:00:00+00:00',
		'group': '',
		'venue': {
			'name': 'Fisht Stadium, Sochi'
		},
		'team1': None,
		'team2': None
	}
	assert_dict(expected, actual[48])
    
def test_get_match(client):
	response = client.simulate_get('/match/35')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-25T21:00:00+00:00',
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
	response = client.simulate_patch('/match/35', body = json.dumps({
		'matchtime': '2018-06-26T21:00:00+00:00'
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-26T21:00:00+00:00',
		'group': 'Group B'
	}
	assert_dict(expected, actual)

	response = client.simulate_patch('/match/35', body = json.dumps({
		'matchtime': '2018-06-25T21:00:00+00:00'
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_venue(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 1
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-25T21:00:00+00:00',
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
	response = client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 24
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_patch_match_teams(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 1,
		'team2_id': 2
	}))
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/match/35'),
		'round': '3',
		'matchtime': '2018-06-25T21:00:00+00:00',
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

def test_patch_match_unknown_match(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 124
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_patch_match_result(client):
	# type: (testing.TestClient) -> None
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
	response = client.simulate_patch('/match/35', body = json.dumps({
		'result': '0-X'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_patch_match_forbidden_field(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_patch('/match/35', body = json.dumps({
		'group': 'Group C'
	}))
	print(response.text)
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
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
		'login': 'jfpoilpret',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, actual[0])
    
def test_get_user_by_id(client):
	response = client.simulate_get('/user/1')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'login': 'jfpoilpret',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, actual)

def test_get_user_by_login(client):
	response = client.simulate_get('/user/jfpoilpret')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'login': 'jfpoilpret',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, actual)

def test_get_user_by_bad_login(client):
	response = client.simulate_get('/user/jfp')
	assert response.status == falcon.HTTP_NOT_FOUND

	# login = fields.String()
	# password = fields.String()
	# fullname = fields.String()
	# email = fields.Email()

def test_post_user(client):
	response = client.simulate_post('/user', body = json.dumps({
		'login': 'dummy',
		'password': 'dummy',
		'fullname': 'Dunny D. Dummy',
		'email': 'dummy@dummy.com',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_CREATED
	
	user =  json.loads(response.text)
	expected = {
		'login': 'dummy',
		'fullname': 'Dunny D. Dummy',
		'email': 'dummy@dummy.com',
		'admin': True,
		'status': 'approved',
		'connection': None
	}
	assert_dict(expected, user)

	#TODO check creation date

	# Check bets
	response = client.simulate_get('/user/%d/bets' % user['id'])
	assert response.status == falcon.HTTP_OK
	bets = json.loads(response.text)
	assert len(bets) == 64
	#TODO further checks all results empty, all matches concerned

	# delete user
	response = client.simulate_delete('/user/%d' % user['id'])
	assert response.status == falcon.HTTP_NO_CONTENT
	
def test_patch_user(client):
	response = client.simulate_patch('/user/jfpoilpret', body = json.dumps({
		'login': 'dummy',
		'password': 'jfpjfp',
		'fullname': 'Dunny D. Dummy',
		'email': 'jfp@gmail.com',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK
	
	user =  json.loads(response.text)
	expected = {
		'login': 'dummy',
		'fullname': 'Dunny D. Dummy',
		'email': 'jfp@gmail.com',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, user)
