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
    # type: () -> testing.TestClient
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

    # response = client.simulate_patch('/match/35', body = json.dumps({
    #     'venue_id': 11
    # }))
    # assert response.status == falcon.HTTP_OK

#TODO also try with a team id that does not exist
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

#TODO also try patchin match with a wrong result format
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
