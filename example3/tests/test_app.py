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
