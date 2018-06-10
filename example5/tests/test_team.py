import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import href

def test_list_teams(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/team')
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
    
def test_get_team(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/team/11')
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
