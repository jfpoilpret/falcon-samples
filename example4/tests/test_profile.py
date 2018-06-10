from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
import base64
import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import href, assert_dict

def test_post_new_profile(client, admin_client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jb007@mi6.uk',
		'password': 'To her Majesty\'s secret service',
		'fullname': 'James Bond'
	}))
	assert response.status == falcon.HTTP_CREATED

	actual = json.loads(response.text)
	expected = {
		'href': href('/profile'),
		'email': 'jb007@mi6.uk',
		'fullname': 'James Bond',
		'score': 0,
	}
	assert_dict(expected, actual)
	assert 'id' in actual.keys()
	assert actual['id'] > 0
	assert 'creation' in actual.keys()
	assert 'connection' in actual.keys()
	# check password is not present
	assert 'password' not in actual.keys()
	assert 'admin' not in actual.keys()
	assert 'status' not in actual.keys()
	# delete user to avoid interfering with other unit tests
	response = admin_client.simulate_delete('/user/%d' % actual['id'])
	assert response.status == falcon.HTTP_NO_CONTENT

def test_post_new_profile_wrong_email(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jb007.mi6.uk',
		'password': 'To her Majesty\'s secret service',
		'fullname': 'James Bond'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_no_fullname(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jb007@mi6.uk',
		'password': 'To her Majesty\'s secret service',
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_no_email(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'password': 'To her Majesty\'s secret service',
		'fullname': 'James Bond'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_no_password(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jb007@mi6.uk',
		'fullname': 'James Bond'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_empty_password(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jb007@mi6.uk',
		'password': '',
		'fullname': 'James Bond'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_duplicate_email(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jfpoilpret@gmail.com',
		'password': 'dummy',
		'fullname': 'James Bond'
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_extra_fields(client):
	# type: (testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'dummy@gmail.com',
		'password': 'dummy',
		'fullname': 'James Bond',
		'status': 'approved',
		'admin': True
	}))
	assert response.status == falcon.HTTP_UNPROCESSABLE_ENTITY

def test_post_new_profile_connection_flow(client, admin_client):
	# type: (testing.TestClient, testing.TestClient) -> None
	response = client.simulate_post('/profile', body = json.dumps({
		'email': 'jfp@dummy.org',
		'password': 'dummy',
		'fullname': 'Jeff'
	}))
	assert response.status == falcon.HTTP_CREATED

	# Try to authenticate (shall be refused)
	token = base64.b64encode('jfp@dummy.org:dummy'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_UNAUTHORIZED

	# Approve user by admin
	response = admin_client.simulate_patch('/user/jfp@dummy.org', body = json.dumps({
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK

	# Try to authenticate (shall be accepted)
	token = base64.b64encode('jfp@dummy.org:dummy'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK

	# Suspend user by admin
	response = admin_client.simulate_patch('/user/jfp@dummy.org', body = json.dumps({
		'status': 'suspended'
	}))
	assert response.status == falcon.HTTP_OK

	# Try to authenticate (shall be refused)
	token = base64.b64encode('jfp@dummy.org:dummy'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_UNAUTHORIZED

	# Self deletion
	#---------------
	# Approve again user by admin
	response = admin_client.simulate_patch('/user/jfp@dummy.org', body = json.dumps({
		'status': 'approved'
	}))
	assert response.status == falcon.HTTP_OK
	# authenticate
	token = base64.b64encode('jfp@dummy.org:dummy'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	assert response.status == falcon.HTTP_OK
	token = json.loads(response.text)['token']
	# delete profile
	client.simulate_delete('/profile', headers = {
		'Authorization': 'Token %s' % token
	})
	assert response.status == falcon.HTTP_OK

	# check user is deleted	
	response = admin_client.simulate_get('/user/jfp@dummy.org')
	assert response.status == falcon.HTTP_NOT_FOUND

def test_get_profile(new_user, better_client):
	# type: (dict, testing.TestClient) -> None
	response = better_client.simulate_get('/profile')
	assert response.status == falcon.HTTP_OK
	profile = json.loads(response.text)
	# check only some fields of new user: email, id, href, fullname, bets, creation
	expected = {
		'href': href('/profile'),
	}
	for key in ('id', 'email', 'fullname', 'bets', 'score', 'creation'):
		expected[key] = new_user[key]
	assert_dict(expected, profile)

def test_patch_profile(better_client):
	# type: (testing.TestClient) -> None
	response = better_client.simulate_patch('/profile', body = json.dumps({
		'fullname': 'Zorro'		
	}))
	assert response.status == falcon.HTTP_OK
	# further check results
	profile = json.loads(response.text)
	assert profile['fullname'] == 'Zorro'
