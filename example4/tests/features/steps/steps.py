from behave import *
from behave.runner import Context
from datetime import datetime
import base64
import falcon
from falcon import testing
import json
import re

class UserClient(object):
	def __init__(self, id, client):
		self.id = id
		self.client = client

@given('system is ready')
def start_system(context):
	# type: (Context) -> None
	# from example4.app import api
	from example4.init_app import create_app
	context.api = api = create_app()
	client = testing.TestClient(api)
	# authenticate admin
	token = base64.b64encode('jfpoilpret:jfp'.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	token = json.loads(response.text)['token']
	client._default_headers = {
		'Authorization': 'Token %s' % token
	}
	context.admin = client
	context.users = {}

@given('user "{user}" exists')
def add_user(context, user):
	# type: (Context, str) -> None
	# create user
	response = context.admin.simulate_post('/user', body = json.dumps({
		'login': user,
		'password': user,
		'status': 'approved',
		'fullname': 'John %s Doe' % user,
		'email': '%s@dummy.com' % user
	}))
	user_id = json.loads(response.text)['id']

	# authenticate new user
	client = testing.TestClient(context.api)
	token = '%s:%s' % (user, user)
	token = base64.b64encode(token.encode('utf-8')).decode('utf-8', 'ignore')
	response = client.simulate_get('/token', headers = {
		'Authorization': 'Basic %s' % token
	})
	token = json.loads(response.text)['token']
	client._default_headers = {
		'Authorization': 'Token %s' % token
	}
	context.users[user] = UserClient(user_id, client)

@given('current date is "{time}"')
def set_time(context, time):
	# type: (Context, str) -> None
	response = context.admin.simulate_patch('/time', body = json.dumps({
		'now': time
	}))
	assert response.status == falcon.HTTP_OK

MATCH_PATTERN = re.compile(r'(.*) - (.*)')

def find_match_in_bets(match, round, bets):
	# type: (str, str, list) -> dict
	m = MATCH_PATTERN.match(match)
	team1 = m.group(1)
	team2 = m.group(2)
	for bet in bets:
		if	bet['match']['round'] == round and \
			bet['match']['team1']['name'] == team1 and \
			bet['match']['team2']['name'] == team2:
			return bet
	return None

def find_match_in_matches(match, round, matches):
	# type: (str, str, list) -> dict
	m = MATCH_PATTERN.match(match)
	team1 = m.group(1)
	team2 = m.group(2)
	for one_match in matches:
		if	one_match['round'] == round and \
			one_match['team1']['name'] == team1 and \
			one_match['team2']['name'] == team2:
			return one_match
	return None

@when('user "{user}" places bets')
def set_bets(context, user):
	# type: (Context, str) -> None
	client = context.users[user].client
	response = client.simulate_get('/bet')
	assert response.status == falcon.HTTP_OK
	all_bets = json.loads(response.text)
	for row in context.table:
		bet = find_match_in_bets(row['match'], row['round'], all_bets)
		assert bet is not None
		response = client.simulate_patch('/bet', body = json.dumps([{
			'id': bet['id'],
			'result': row['result']
		}]))
		assert response.status == falcon.HTTP_OK

@when('admin sets match results')
def set_match_results(context):
	# type: (Context) -> None
	client = context.admin
	response = client.simulate_get('/match')
	assert response.status == falcon.HTTP_OK
	all_matches = json.loads(response.text)
	for row in context.table:
		match = find_match_in_matches(row['match'], row['round'], all_matches)
		assert match is not None
		response = client.simulate_patch('/match/%d' % match['id'], body = json.dumps({
			'result': row['result']
		}))
		assert response.status == falcon.HTTP_OK

@then('user "{user}" bets should match')
def check_bets(context, user):
	# type: (Context, str) -> None
	client = context.users[user].client
	response = client.simulate_get('/bet')
	assert response.status == falcon.HTTP_OK
	all_bets = json.loads(response.text)
	for row in context.table:
		bet = find_match_in_bets(row['match'], row['round'], all_bets)
		assert bet is not None
		assert bet['result'] == row['result']

@then('user "{user}" score should be {score:d}')
def check_user_score(context, user, score):
	# type: (Context, str, int) -> None
	client = context.admin
	response = client.simulate_get('/user/%s' % user)
	assert response.status == falcon.HTTP_OK
	the_user = json.loads(response.text)
	print("actual score %d" % the_user['score'])
	print("expected score %d" % score)
	assert json.loads(response.text)['score'] == score
