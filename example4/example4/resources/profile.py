import falcon
import logging
from marshmallow import fields, validates, ValidationError
from ..utils import URLFor, StrictSchema, update_item_fields, TimeBase, hash_password
from .resource import Resource
from ..model import DBBet, DBMatch, DBUser

logger = logging.getLogger(__name__)

class ProfileSchema(StrictSchema):
	id = fields.Integer()
	href = URLFor('/profile')
	email = fields.Email()
	fullname = fields.String()
	#TODO /profile/bets instead?
	bets = URLFor('/bets')
	score = fields.Integer()
	creation = fields.DateTime()
	connection = fields.DateTime()

class ProfilePostSchema(StrictSchema):
	email = fields.Email(required = True)
	password = fields.String(required = True)
	fullname = fields.String(required = True)

	@validates('password')
	def verify_result(self, value):
		if not value:
			logger.info('ProfilePostSchema empty \'password\'')
			raise ValidationError('password must not be empty', 'password')

class ProfilePatchSchema(StrictSchema):
	email = fields.Email()
	password = fields.String()
	fullname = fields.String()

	@validates('password')
	def verify_result(self, value):
		if not value:
			logger.info('ProfilePatchSchema empty \'password\'')
			raise ValidationError('password must not be empty', 'password')

class Profile(Resource):
	schema = ProfileSchema()
	post_request_schema = ProfilePostSchema()
	patch_request_schema = ProfilePatchSchema()

	# To allow self registration with POST, no authorization is required here
	auth = {
		'exempt_methods': 'POST'
	}

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		Resource.__init__(self, timebase)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		self.check_and_set_result(req, 'profile', self.get_user(req.context['user'].id))

	def on_post(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		input = req.context['json']
		user = DBUser(	email = input['email'],
						password = hash_password(input['password']),
						status = 'pending',
						admin = False,
						fullname = input['fullname'],
						creation = self.now())
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

	def on_patch(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		user = self.check_result('profile', self.get_user(req.context['user'].id))
		values = req.context['json']
		# hash password if modified
		if 'password' in values.keys():
			values['password'] = hash_password(values['password'])
		if update_item_fields(user, Profile.patch_request_schema.fields, values):
			session = self.session()
			session.add(user)
			session.commit()
			session.refresh(user)
		req.context['result'] = user

	def on_delete(self, req, resp):
		# type: (falcon.Request, falcon.Response, str) -> None
		user = req.context['user']
		# delete all bets
		self.session().query(DBBet).filter_by(better_id = user.id).delete(synchronize_session = False)
		self.session().delete(user)
		self.session().commit()
		resp.status = falcon.HTTP_NO_CONTENT
