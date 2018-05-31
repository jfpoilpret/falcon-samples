import falcon
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema
from ..utils.marshmallow_util import URLFor, StrictSchema
from ..utils.falcon_util import update_item_fields
from ..utils.timebase import TimeBase
from ..model import DBBet, DBUser

class BetSchema(StrictSchema):
	id = fields.Integer()
	href = URLFor('/bet/{id}')
	bettime = fields.DateTime()
	match = fields.Nested('MatchSchema')
	result = fields.String()

class Bets(object):
	schema = BetSchema(many = True)

	def session(self):
		# type: () -> Session
		return self._session

	def on_get(self, req, resp, id_or_name):
		# type: (falcon.Request, falcon.Response, str) -> None
		user = self._load_user(id_or_name)
		if not user:
			resp.status = falcon.HTTP_NOT_FOUND
			return
		bets = self.session().query(DBBet).filter_by(better_id = user.id).all()
		req.context['result'] = bets

	#TODO Authorize multiple PATCH?

	def _load_user(self, id_or_name):
		# type: (str) -> DBUser
		if id_or_name.isnumeric():
			return self.session().query(DBUser).filter_by(id = int(id_or_name)).one_or_none()
		else:
			return self.session().query(DBUser).filter_by(login = id_or_name).one_or_none()

class Bet(object):
	schema = BetSchema()

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		self._timebase = timebase

	def session(self):
		# type: () -> Session
		return self._session

	def on_get(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		bet = self.session().query(DBBet).filter_by(id = id).one_or_none()
		if not bet:
			resp.status = falcon.HTTP_NOT_FOUND
			return
		if bet.better_id != req.context['user'].id:
			resp.status = falcon.HTTP_FORBIDDEN
			return
		req.context['result'] = bet

	def on_patch(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		pass

	def _load_user(self, id_or_name):
		# type: (str) -> DBUser
		if id_or_name.isnumeric():
			return self.session().query(DBUser).filter_by(id = int(id_or_name)).one_or_none()
		else:
			return self.session().query(DBUser).filter_by(login = id_or_name).one_or_none()
