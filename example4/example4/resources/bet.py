import falcon
import logging
import re
from marshmallow import fields, Schema, validates, ValidationError
from ..utils.marshmallow_util import URLFor, StrictSchema
from ..utils.falcon_util import update_item_fields
from ..utils.timebase import TimeBase
from ..model import DBBet
from .resource import Resource

logger = logging.getLogger(__name__)

class BetSchema(Schema):
	id = fields.Integer()
	better = fields.Nested('UserSchema')
	bettime = fields.DateTime()
	match = fields.Nested('MatchSchema')
	result = fields.String()

RESULT_PATTERN = re.compile(r'([1-9]?[0-9])-([1-9]?[0-9])')

class BetPatchSchema(StrictSchema):
	id = fields.Integer()
	result = fields.String()

	@validates('result')
	def verify_result(self, value):
		if value and not RESULT_PATTERN.match(value):
			logger.info('BetPatchSchema bad \'result\' format for %s', value)
			raise ValidationError('result must comply to format "0-0"', 'result')

class Bets(Resource):
	schema = BetSchema(many = True)
	patch_request_schema = BetPatchSchema(many = True)

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		Resource.__init__(self, timebase)

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
		now = self.now()
		past_match_ids = [id for id, bet in patched_bets.items() if bet.match.matchtime <= now]
		if past_match_ids:
			resp.status = falcon.HTTP_FORBIDDEN
			#TODO add error message?
			return
			
		# ensure match is already known (teams not "virtual")
		unknown_match_ids = [id for id, bet in patched_bets.items() 
			if bet.match.team1.group == 'virtual' or bet.match.team2.group == 'virtual']
		if unknown_match_ids:
			resp.status = falcon.HTTP_UNPROCESSABLE_ENTITY
			#TODO add error message?
			return
		
		# update patched bets
		session = self.session()
		for id, bet in patched_bets.items():
			bet.bettime = now
			bet.result = new_bets[id]
			# calculate utility columns winner and goals_diff
			result = RESULT_PATTERN.match(bet.result)
			goals1 = int(result.group(1))
			goals2 = int(result.group(2))
			if goals1 > goals2:
				bet.winner = 1
				bet.goals_diff = goals1 - goals2
			elif goals1 < goals2:
				bet.winner = 2
				bet.goals_diff = goals2 - goals1
			else:
				bet.winner = 0
				bet.goals_diff = 0
			session.add(bet)
			session.commit()
			session.refresh(bet)
		req.context['result'] = patched_bets.values()
