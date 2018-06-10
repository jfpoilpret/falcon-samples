import falcon
import logging
import re
from marshmallow import fields, Schema, validates, ValidationError
from ..utils import URLFor, StrictSchema, update_item_fields, TimeBase
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
	id = fields.Integer(required = True)
	result = fields.String(required = True)

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
			raise falcon.HTTPForbidden(description = \
				'The following bets ids do not exist (or do not belong to you): %s' % ','.join(map(str, bad_ids)))

		# filter bets to be changed
		patched_bets = {id: bet for id, bet in bets.items() if id in new_bets.keys()}

		# ensure all bets are for future matches!
		now = self.now()
		past_match_ids = [id for id, bet in patched_bets.items() if bet.match.matchtime <= now]
		if past_match_ids:
			raise falcon.HTTPForbidden(description = \
				'The following bets ids are related to past matches, ' + \
				'you are not allowed to place bets on them: %s' % ','.join(map(str, past_match_ids)))
			
		# ensure match is already known (teams not "virtual")
		unknown_match_ids = [id for id, bet in patched_bets.items() 
			if bet.match.team1.group == 'virtual' or bet.match.team2.group == 'virtual']
		if unknown_match_ids:
			raise falcon.HTTPUnprocessableEntity(
				description = 'The following bets ids relate to match which teams are still not known, ' + \
				'you are not allowed to place bets on them: %s' % ','.join(map(str, unknown_match_ids)))
		
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
