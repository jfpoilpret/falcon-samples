from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
import falcon
from falcon import testing
from falcon.testing import helpers
import json
from .utils import set_time_base

def test_get_time(admin_client):
	# type: (testing.TestClient) -> None
	response = admin_client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK

	actual = json.loads(response.text)
	assert actual['delta'] == 0

	now = parse_date(actual['now'])
	delta = now - datetime.now(timezone.utc)
	assert -2 < delta.total_seconds() < +2

def test_patch_time_base(admin_client):
	# type: (testing.TestClient) -> None
	base = '2018-01-01T14:30:00+00:00'
	set_time_base(admin_client, base)
	base = parse_date(base)
	delta = base - datetime.now(timezone.utc)

	response = admin_client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert -2 < actual['delta'] - delta.total_seconds() < 2

	now = parse_date(actual['now'])
	delta = base - now
	assert -2 < delta.total_seconds() < +2

	response = admin_client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK

def test_patch_time_delta(admin_client):
	# type: (testing.TestClient) -> None
	base = parse_date('2018-01-01T14:30:00+00:00')
	delta = (base - datetime.now(timezone.utc)).total_seconds()
	response = admin_client.simulate_patch('/time', body = json.dumps({
		'delta': delta
	}))
	assert response.status == falcon.HTTP_OK

	response = admin_client.simulate_get('/time')
	assert response.status == falcon.HTTP_OK
	actual = json.loads(response.text)
	assert -2 < actual['delta'] - delta < 2

	now = parse_date(actual['now'])
	delta = base - now
	assert -2 < delta.total_seconds() < +2

	response = admin_client.simulate_delete('/time')
	assert response.status == falcon.HTTP_OK
