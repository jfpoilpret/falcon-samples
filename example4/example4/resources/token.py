
import falcon
from marshmallow import Schema, fields
from falcon_auth import BasicAuthBackend
from ..utils import Authenticator
# from ..utils.auth import Authenticator

class TokenSchema(Schema):
	token = fields.UUID()
	expiry = fields.DateTime()

class Token(object):
	schema = TokenSchema()
	auth = {
		'backend': BasicAuthBackend(Authenticator.instance)
	}

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		token, expiry = Authenticator.instance.new_token(req.context['user'])
		req.context['result'] = {
			'token': token,
			'expiry': expiry
		}
