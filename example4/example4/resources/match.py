import logging
import re
import falcon
from sqlalchemy import inspect
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema, validates, ValidationError
from ..utils.marshmallow_util import URLFor, StrictSchema
from ..utils.falcon_util import update_item_fields
from ..model import DBBet, DBMatch

logger = logging.getLogger(__name__)

class MatchSchema(Schema):
	id = fields.Integer()
	href = URLFor('/match/{id}')
	round = fields.String()
	matchtime = fields.DateTime()
	venue = fields.Nested('VenueSchema')
	team1 = fields.Nested('TeamSchema')
	team2 = fields.Nested('TeamSchema')
	group = fields.String()
	result = fields.String()

RESULT_PATTERN = re.compile(r'([1-9]?[0-9])-([1-9]?[0-9])')

class MatchPatchSchema(StrictSchema):
	matchtime = fields.DateTime()
	venue_id = fields.Integer()
	team1_id = fields.Integer()
	team2_id = fields.Integer()
	result = fields.String(allow_none=True)

	@validates('result')
	def verify_result(self, value):
		if value and not RESULT_PATTERN.match(value):
			logger.info('MatchPatchSchema bad \'result\' format for %s', value)
			raise ValidationError('result must comply to format "0-0"', 'result')

class Matches(object):
	schema = MatchSchema(many = True)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self._session.query(DBMatch).all()

class Match(object):
	schema = MatchSchema()
	patch_request_schema = MatchPatchSchema()

	def session(self):
		# type: () -> Session
		return self._session

	def on_get(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		match = self.session().query(DBMatch).filter_by(id = id).one_or_none()
		if match:
			req.context['result'] = match
		else:
			resp.status = falcon.HTTP_NOT_FOUND

	#FIXME prevent setting result of future match!
	def on_patch(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		if not req.context['user'].admin:
			resp.status = falcon.HTTP_FORBIDDEN
			return
		session = self.session()
		match = session.query(DBMatch).filter_by(id = id).one_or_none()
		if match:
			values = req.context['json']
			if update_item_fields(match, Match.patch_request_schema.fields, values):
				session.add(match)
				session.commit()
				session.refresh(match)

				if match.result:
					winner, goals_winner, goals_loser, goals_diff = self._compute_result(match)
					# update team points if match is during rounds 1,2,3
					if match.group in ['1', '2', '3']:
						self._update_points(match.team1, 1, winner, goals_winner, goals_loser)
						self._update_points(match.team2, 2, winner, goals_winner, goals_loser)
						session.refresh(match)

					#TODO small refactoring needed?
					# batch update of all bets for this match
					bets = inspect(DBBet).local_table
					connection = session.connection()
					# Perform updates for exact results (score 3)
					update = bets.update().where(bets.c.match_id == match.id).\
						where(bets.c.result == match.result).\
						values(score = 3)
					connection.execute(update)
					# Perform updates for correct results with same goals difference (score 2)
					update = bets.update().where(bets.c.match_id == match.id).\
						where(bets.c.winner == winner).where(bets.c.goals_diff == goals_diff).\
						values(score = 2)
					connection.execute(update)
					# Perform updates for correct bet on winner (score 1)
					update = bets.update().where(bets.c.match_id == match.id).\
						where(bets.c.winner == winner).where(bets.c.goals_diff != goals_diff).\
						values(score = 1)
					connection.execute(update)
					# Perform updates for lost bets (score 0)
					update = bets.update().where(bets.c.match_id == match.id).\
						where(bets.c.result is not None).where(bets.c.winner != winner).\
						values(score = 0)
					connection.execute(update)
			req.context['result'] = match
		else:
			resp.status = falcon.HTTP_NOT_FOUND

	def _update_points(self, team, num_team, winner, goals_winner, goals_loser):
		if winner == 0:
			team.drawn = team.drawn + 1
			team.points = team.points + 1
			team.goals_for = goals_winner
			team.goals_against = goals_loser
		elif num_team == winner:
			team.won = team.won + 1
			team.points = team.points + 3
			team.goals_for = goals_winner
			team.goals_against = goals_loser
		else:
			team.lost = team.lost + 1
			team.goals_for = goals_loser
			team.goals_against = goals_winner
		self.session().add(team)
		self.session().commit()

	def _compute_result(self, match):
		result = RESULT_PATTERN.match(match.result)
		goals1 = int(result.group(1))
		goals2 = int(result.group(2))
		if goals1 > goals2:
			return (1, goals1, goals2, goals1 - goals2)
		elif goals1 < goals2:
			return (2, goals2, goals1, goals2 - goals1)
		else:
			return (0, goals1, goals1, 0)
