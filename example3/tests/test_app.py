import falcon
from falcon import testing
from falcon.testing import helpers
import json
import pytest
from datetime import datetime

from example3.app import api

def href(path):
    return 'http://' + helpers.DEFAULT_HOST + path

@pytest.fixture
def client():
    return testing.TestClient(api)

def assert_dict(expected, actual):
    for key, value in expected.items():
        print("assert_dict() %s %s" % (key, str(value)))
        if isinstance(value, dict):
            assert_dict(value, actual[key])
        else:
            assert value == actual[key]

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
        'round': '3',
        'matchtime': '2018-06-25T21:00:00+00:00',
        'group': 'Group B',
        'venue': {
            'name': 'Saransk Stadium'
        },
        'team1': {
            'name': 'Iran'
        },
        'team2': {
            'name': 'Portugal'
        }
    }
    assert_dict(expected, actual)

#TODO test patch one match
