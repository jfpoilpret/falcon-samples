from marshmallow import Schema, fields
from falcon_auth import BasicAuthBackend
from .utils.auth import Authenticator

class TokenSchema(Schema):
	token = fields.UUID()
	expiry = fields.DateTime()

class Token(object):
	schema = TokenSchema()
	auth = {
		'backend': BasicAuthBackend(Authenticator.instance)
	}

	def on_get(self, req, resp):
		print('Token.on_get() #1')
		token, expiry = Authenticator.instance.new_token(req.context['user'])
		print('Token.on_get() #2')
		req.context['result'] = {
			'token': token,
			'expiry': expiry
		}
		print('Token.on_get() #3')
