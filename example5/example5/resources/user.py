import falcon
import logging
from marshmallow import fields, Schema, validates, ValidationError
from ..utils import URLFor, StrictSchema, update_item_fields, TimeBase, hash_password
from .resource import Resource
from ..model import DBBet, DBMatch, DBUser

logger = logging.getLogger(__name__)

class UserSchema(StrictSchema):
	id = fields.Integer()
	href = URLFor('/user/{id}')
	email = fields.Email()
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String()
	bets = URLFor('/bets')
	score = fields.Integer()
	creation = fields.DateTime()
	connection = fields.DateTime()

class UserPostSchema(StrictSchema):
	email = fields.Email(required = True)
	password = fields.String(required = True)
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String(required = True)

	@validates('status')
	def verify_result(self, value):
		if value not in ('pending', 'approved', 'suspended'):
			logger.info('UserPostSchema incorrect \'status\' value \'%s\'' % value)
			raise ValidationError('status must be one of \'pending\', \'approved\', \'suspended\'', 'status')

	@validates('password')
	def verify_result(self, value):
		if not value:
			logger.info('UserPostSchema empty \'password\'')
			raise ValidationError('password must not be empty', 'password')

class UserPatchSchema(StrictSchema):
	email = fields.Email()
	password = fields.String()
	status = fields.String()
	admin = fields.Boolean()
	fullname = fields.String()

	@validates('status')
	def verify_result(self, value):
		if value not in ('pending', 'approved', 'suspended'):
			logger.info('UserPostSchema incorrect \'status\' value \'%s\'' % value)
			raise ValidationError('status must be one of \'pending\', \'approved\', \'suspended\'', 'status')

	@validates('password')
	def verify_result(self, value):
		if not value:
			logger.info('UserPatchSchema empty \'password\'')
			raise ValidationError('password must not be empty', 'password')

class Users(Resource):
	schema = UserSchema()
	get_schema = UserSchema(many = True)
	post_request_schema = UserPostSchema()

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		Resource.__init__(self, timebase)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		self.check_admin(req)
		req.context['result'] = self.session().query(DBUser).all()

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

class User(Resource):
	schema = UserSchema()
	patch_request_schema = UserPatchSchema()

	def on_get(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, str) -> None
		self.check_admin(req)
		self.check_and_set_result(req, 'user', self.get_user(id_or_name))

	def on_patch(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, int) -> None
		# only admin can modify a user
		self.check_admin(req)
		user = self.check_result('user', self.get_user(id_or_name))
		values = req.context['json']

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
