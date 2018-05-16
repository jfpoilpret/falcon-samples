import falcon
from falcon import testing
import json
import pytest

from example3.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)

def test_list_teams(client):
    response = client.simulate_get('/team')
    assert response.status == falcon.HTTP_OK

    actual = json.loads(response.text)
    assert len(actual) == 32
    expected = {
        'id': 1,
        'name': 'Egypt',
        'group': 'Group A'
    }
    assert actual[0] == expected
    expected = {
        'id': 32,
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
        'id': 1,
        'name': 'Ekaterinburg Stadium',
    }
    assert actual[0] == expected
    expected = {
        'id': 12,
        'name': 'Volgograd Stadium',
    }
    assert actual[11] == expected
    
def test_get_venue(client):
    response = client.simulate_get('/venue/5')
    assert response.status == falcon.HTTP_OK

    actual = json.loads(response.text)
    expected = {
        'id': 5,
        'name': 'Luzhniki Stadium, Moscow',
    }
    assert actual == expected

def test_list_matches(client):
    response = client.simulate_get('/match')
    assert response.status == falcon.HTTP_OK

    actual = json.loads(response.text)
    assert len(actual) == 64

    #TODO more assertions on a few matches: venue, teams, time
    
