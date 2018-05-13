import falcon
from falcon import testing
import json
import pytest

from example2.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)

def test_list_teams(client):
    expected = [
        {
            "id": 1,
            "name": "France"
        },
        {
            "id": 2,
            "name": "Germany"
        },
        {
            "id": 3,
            "name": "England"
        }
    ]

    response = client.simulate_get('/team')
    assert response.status == falcon.HTTP_OK

    actual = json.loads(response.text)
    assert actual == expected

def test_create_team(client):
    new_team = {
        'name': 'Spain'
    }
    response = client.simulate_post(
        '/team',
        body = json.dumps(new_team)
    )

    assert response.status == falcon.HTTP_CREATED
    created_team = json.loads(response.text)
    assert created_team['name'] == 'Spain'

def test_delete_team(client):
    response =  client.simulate_delete('/team/9999')
    assert response.status == falcon.HTTP_NOT_FOUND
    response =  client.simulate_delete('/team/4')
    assert response.status == falcon.HTTP_NO_CONTENT
