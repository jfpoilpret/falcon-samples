from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import href, assert_dict

def test_post_new_profile(client):
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

#TODO check it is not possible to connect until approval

def test_delete_new_profile(new_user, better_client):
	pass

def test_patch_profile():
	pass

def test_get_profile():
	pass

# def test_patch_user(admin_client):
# 	# type: (testing.TestClient) -> None
# 	response = admin_client.simulate_patch('/user/jfpoilpret@gmail.com', body = json.dumps({
# 		'email': 'jfp@gmail.com',
# 		'password': 'jfpjfp',
# 		'fullname': 'Dunny D. Dummy',
# 		'admin': True,
# 		'status': 'approved'
# 	}))
# 	assert response.status == falcon.HTTP_OK
	
# 	user =  json.loads(response.text)
# 	expected = {
# 		'email': 'jfp@gmail.com',
# 		'fullname': 'Dunny D. Dummy',
# 		'admin': True,
# 		'status': 'approved'
# 	}
# 	assert_dict(expected, user)

# 	response = admin_client.simulate_patch('/user/jfp@gmail.com', body = json.dumps({
# 		'email': 'jfpoilpret@gmail.com',
# 		'password': 'jfp',
# 		'fullname': 'Jean-Francois Poilpret',
# 		'admin': True,
# 		'status': 'approved'
# 	}))
# 	assert response.status == falcon.HTTP_OK
