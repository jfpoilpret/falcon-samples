import falcon
from falcon import testing
import json
import pytest

from example1.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)

def test_list_teams(client):
    expected = {
        'teams': [
            {
                'name': 'France',
                'href': '/team/1'
            }
        ]
    }

    response = client.simulate_get('/team')
    assert response.status == falcon.HTTP_OK

    actual = json.loads(response.text)
    assert actual == expected

