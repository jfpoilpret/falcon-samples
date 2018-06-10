import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import href, assert_dict

def test_list_venues(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/venue')
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
    
def test_get_venue(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/venue/5')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/venue/5'),
		'id': 5,
		'name': 'Luzhniki Stadium, Moscow',
	}
	assert actual == expected
