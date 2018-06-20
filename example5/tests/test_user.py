from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import href, assert_dict

def test_list_users(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/user')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert len(actual) == 1
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'email': 'jfpoilpret@gmail.com',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved',
	}
	assert_dict(expected, actual[0])
	# check password is not present
	assert 'password' not in actual[0].keys()
    
def test_get_user_by_id(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/user/1')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'email': 'jfpoilpret@gmail.com',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved',
	}
	assert_dict(expected, actual)

def test_get_user_by_login(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/user/jfpoilpret@gmail.com')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	expected = {
		'href': href('/user/1'),
		'id': 1,
		'email': 'jfpoilpret@gmail.com',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, actual)

def test_get_user_by_bad_login(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/user/jfp@jfp.org')
	assert response.status == falcon.HTTP_NOT_FOUND

def test_post_user(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_post('/user', body = json.dumps({
		'email': 'dummy@dummy.com',
		'password': 'dummy',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_CREATED
	
	user =  json.loads(response.text)
	expected = {
		'email': 'dummy@dummy.com',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved',
		'score': 0,
		'connection': None
	}
	assert_dict(expected, user)

	# check creation date
	creation = parse_date(user['creation'])
	delta = creation - datetime.now(timezone.utc)
	assert -4 < delta.total_seconds() < +4

	# delete user
	response = admin_client.simulate_delete('/user/%d' % user['id'])
	assert response.status == falcon.HTTP_NO_CONTENT

def test_patch_user(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_patch('/user/jfpoilpret@gmail.com', body = json.dumps({
		'email': 'jfp@gmail.com',
		'password': 'jfpjfp',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK
	
	user =  json.loads(response.text)
	expected = {
		'email': 'jfp@gmail.com',
		'fullname': 'Dunny D. Dummy',
		'admin': True,
		'status': 'approved'
	}
	assert_dict(expected, user)

	response = admin_client.simulate_patch('/user/jfp@gmail.com', body = json.dumps({
		'email': 'jfpoilpret@gmail.com',
		'password': 'jfp',
		'fullname': 'Jean-Francois Poilpret',
		'admin': True,
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK
