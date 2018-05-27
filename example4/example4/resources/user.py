import falcon
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema
from ..utils.marshmallow_util import URLFor, StrictSchema
from ..utils.falcon_util import update_item_fields
from ..model import DBUser

#TODO improve read/write fields, hide some field depending on who is authenticated
class UserSchema(StrictSchema):
	id = fields.Integer()
	href = URLFor('/user/{id}')
	login = fields.String()
	password = fields.String()
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String()
	email = fields.Email()
	creation = fields.DateTime()
	connection = fields.DateTime()

class UserPatchSchema(StrictSchema):
	login = fields.String()
	password = fields.String()
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String()
	email = fields.Email()

class Users(object):
	schema = UserSchema(many = True)

	def session(self):
		""" :type: sqlalchemy.orm.Session"""
		# type: () -> Session
		return self._session

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self.session().query(DBUser).all()

	#TODO no authentication required (user registration)
	def on_post(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		#TODO
		pass

class User(object):
	get_schema = UserSchema()
	patch_request_schema = UserPatchSchema()

	def session(self):
		""" :type: sqlalchemy.orm.Session"""
		# type: () -> Session
		return self._session

	def on_get(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, str) -> None
		if id_or_name.isnumeric():
			user = self.session().query(DBUser).filter_by(id = int(id_or_name)).one_or_none()
		else:
			user = self.session().query(DBUser).filter_by(login = id_or_name).one_or_none()
		if user:
			req.context['result'] = user
		else:
			resp.status = falcon.HTTP_NOT_FOUND

	#TODO patch (some fields for admin only, some field for user themselves)
	def on_patch(self, req, resp, id_or_name):
		pass
		
	def get_user(self, login):
		return self.session().query(DBUser).filter_by(login = login).one_or_none
