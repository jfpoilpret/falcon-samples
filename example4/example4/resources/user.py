import falcon
from marshmallow import fields, Schema
from ..utils import URLFor, StrictSchema, update_item_fields, TimeBase, hash_password
from .resource import Resource
from ..model import DBBet, DBMatch, DBUser

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
	bets = URLFor('/bets')
	score = fields.Integer()
	creation = fields.DateTime()
	connection = fields.DateTime()

class UserPostSchema(StrictSchema):
	login = fields.String(required = True)
	password = fields.String(required = True)
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String(required = True)
	email = fields.Email(required = True)

class UserPatchSchema(StrictSchema):
	login = fields.String()
	password = fields.String()
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String()
	email = fields.Email()

class Users(Resource):
	schema = UserSchema()
	get_schema = UserSchema(many = True)
	post_request_schema = UserPostSchema()

	#TODO implement self-registration POST later; for the moment, jus allow admin to create users
	#NOTE it is probably better toc reate a new resource "regitration" specifically for anonymous users
	# # POST is used for self registration of new users
	# auth = {
	# 	'exempt_methods': 'POST'
	# }

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		Resource.__init__(self, timebase)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self.session().query(DBUser).all()

	#TODO (later) check who is creating user: self registration or admin
	def on_post(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		self.check_admin(req)
		user = DBUser(**req.context['json'])
		user.password = hash_password(user.password)
		user.creation = self.now()
		self.session().add(user)
		self.session().commit()
		self.session().refresh(user)
		# create all bets for this user
		matches = self.session().query(DBMatch.id).all()
		for match in matches:
			bet = DBBet(better_id = user.id, match_id = match.id)
			self.session().add(bet)
			self.session().commit()
		req.context['result'] = user
		resp.status = falcon.HTTP_CREATED

#TODO missing method to get oneself?
class User(Resource):
	schema = UserSchema()
	patch_request_schema = UserPatchSchema()

	def on_get(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, str) -> None
		self.check_and_set_result(req, 'user', self.get_user(id_or_name))

	def on_patch(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, int) -> None
		# only admin or user can modify himself
		user = self.check_result('user', self.get_user(id_or_name))
		values = req.context['json']
		if self.is_admin(req):
			pass
		elif req.context['user'].id == user.id:
			# check only some fields (fullname, password) are patched
			extra = values.keys() - ('fullname', 'password') 
			if extra:
				raise falcon.HTTPUnprocessableEntity('The following fields cannot be patched: %s' % ','.join(extra))
		else:
			# user is neither admin nor owner of the patched user
			raise falcon.HTTPForbidden(description = 'Only an administrator can perform this action.')

		# hash password if modified
		if 'password' in values.keys():
			values['password'] = hash_password(values['password'])
		if update_item_fields(user, User.patch_request_schema.fields, values):
			session = self.session()
			session.add(user)
			session.commit()
			session.refresh(user)
		req.context['result'] = user

	def on_delete(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, str) -> None
		self.check_admin(req)
		user = self.check_result('user', self.get_user(id_or_name))
		# delete all bets
		self.session().query(DBBet).filter_by(better_id = user.id).delete(synchronize_session = False)
		self.session().delete(user)
		self.session().commit()
		resp.status = falcon.HTTP_NO_CONTENT
