from falcon_auth import BasicAuthBackend
from .init_app import authenticator

class Token(object):
	auth = {
		'backend': BasicAuthBackend(authenticator)
	}

	def on_get(self, req, resp):
		token, expiry = authenticator.new_token(req.context['user'])
		req.context['result'] = {
			'token': token,
			'expiry': expiry
		}
