import falcon
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema
from ..utils.marshmallow_util import URLFor, StrictSchema
from ..utils.falcon_util import update_item_fields
from ..utils.timebase import TimeBase
from ..model import DBBet, DBUser

class BetSchema(Schema):
	id = fields.Integer()
	better = fields.Nested('UserSchema')
	bettime = fields.DateTime()
	match = fields.Nested('MatchSchema')
	result = fields.String()

class BetPatchSchema(StrictSchema):
	id = fields.Integer()
	result = fields.String()

class Bets(object):
	schema = BetSchema(many = True)
	patch_request_schema = BetPatchSchema(many = True)

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		self._timebase = timebase

	def session(self):
		# type: () -> Session
		return self._session

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		user = req.context['user']
		bets = self.session().query(DBBet).filter_by(better_id = user.id).all()
		req.context['result'] = bets

	def on_patch(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		new_bets = {bet['id']: bet['result'] for bet in req.context['json']}
		user = req.context['user']
		bets = self.session().query(DBBet).filter_by(better_id = user.id).all()
		bets = {bet.id: bet for bet in bets}

		# check all bets to be patched belong to current user
		bad_ids = new_bets.keys() - bets.keys()
		if bad_ids:
			resp.status = falcon.HTTP_FORBIDDEN
			#TODO add error message?
			return
		# filter bets to be changed
		patched_bets = {id: bet for id, bet in bets.items() if id in new_bets.keys()}

		# ensure all bets are for future matches!
		now = self._timebase.now()
		past_match_ids = [id for id, bet in patched_bets.items() if bet.match.matchtime <= now]
		if past_match_ids:
			resp.status = falcon.HTTP_FORBIDDEN
			#TODO add error message?
			return
			
		# ensure match is already known (teams not null)
		unknown_match_ids = [id for id, bet in patched_bets.items() if bet.match.team1_id is None or bet.match.team2_id is None]
		if unknown_match_ids:
			resp.status = falcon.HTTP_UNPROCESSABLE_ENTITY
			#TODO add error message?
			return
		
		# update patched bets
		session = self.session()
		for id, bet in patched_bets.items():
			bet.bettime = now
			bet.result = new_bets[id]
			session.add(bet)
			session.commit()
			session.refresh(bet)
		req.context['result'] = patched_bets.values()
