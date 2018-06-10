import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import href, assert_dict, set_time_base

def test_list_matches(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/match')
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
    
def test_get_match(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/match/35')
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

def test_patch_match_time(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
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

	response = admin_client.simulate_patch('/match/35', body = json.dumps({
		'matchtime': '2018-06-25T18:00:00+00:00'
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_venue(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
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

	response = admin_client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 11
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_unknown_venue(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
		'venue_id': 24
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'title': 'Integrity constraint error'
	}
	assert_dict(expected, actual)

def test_patch_match_teams(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
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

	response = admin_client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 5,
		'team2_id': 7
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_unknown_team(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-01T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
		'team1_id': 124
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'title': 'Integrity constraint error'
	}
	assert_dict(expected, actual)

def test_patch_match_result(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-26T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
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

	response = admin_client.simulate_patch('/match/35', body = json.dumps({
		'result': None
	}))
	assert response.status == falcon.HTTP_OK

def test_patch_match_incorrect_result(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-26T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
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

def test_patch_future_match_result(admin_client):
	# type: (testing.TestClient) -> None
	set_time_base(admin_client, '2018-06-26T00:00:00+00:00')
	response = admin_client.simulate_patch('/match/64', body = json.dumps({
		'result': '0-1'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY
	actual = json.loads(response.text)
	print('actual %s' % str(actual))
	expected = {
		'description': 'This match has not been played yet, it is not allowed to set its result.'
	}
	assert_dict(expected, actual)

def test_patch_match_forbidden_field(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_patch('/match/35', body = json.dumps({
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
