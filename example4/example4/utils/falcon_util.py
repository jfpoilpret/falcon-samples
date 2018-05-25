import logging
from falcon import HTTPError, Request, Response

logger = logging.getLogger(__name__)

def update_item_fields(item, keys, values):
	# type: (dict, list, dict) -> bool
	update = False
	for key in keys:
		if key in values.keys():
			setattr(item, key, values[key])
			update = True
	return update

class ExceptionHandler(object):
	def __init__(self, status, title):
		# type: (str, str) -> None
		self._status = status
		self._title = title

	def __call__(self, ex, req, resp, params):
		# type: (Exception, Request, response, dict) -> None
		logger.warning('Exception occurred on request %s %s', req.method, req.uri, exc_info = ex)
		raise HTTPError(self._status, self._title, str(ex))

class LoggingMiddleware(object):
	def process_request(self, req, resp):
		# type: (Request, Response) -> None
		logger.debug('Received: %s %s', req.method, req.uri)

	def process_resource(self, req, resp, resource, params):
		# type: (Request, Response, object, dict) -> None
		logger.debug('Dispatched: %s %s to %s', req.method, req.uri, resource.__class__.__name__)

	def process_response(sel, req, resp, resource, req_succeeded):
		# type: (Request, Response, object, bool) -> None
		if 'user' in req.context:
			user = req.context['user']
			user = '%s (%d)' % (user.login, user.id)
		else:
			user = 'no user'
		logger.debug('Response for: %s %s succeeded for %s', req.method, req.uri, 'succeeded' if req_succeeded else 'failed', user)
