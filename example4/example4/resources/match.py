import logging
import re
import falcon
from sqlalchemy import inspect, or_
from sqlalchemy.sql import func, select
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema, validates, ValidationError
from ..utils.marshmallow_util import URLFor, StrictSchema
from ..utils.falcon_util import update_item_fields
from ..model import DBBet, DBMatch, DBTeam, DBUser

logger = logging.getLogger(__name__)

class MatchSchema(Schema):
	id = fields.Integer()
	href = URLFor('/match/{id}')
	matchnumber = fields.Integer()
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
				# if result is known, then update result-dependent attributes
				self._update_match_score(match)
				# save match changes
				session.add(match)
				session.commit()
				session.refresh(match)

				if match.result:
					if match.round in ['1', '2', '3']:
						# if this is a group match, then update points for team1 and teams2
						self._update_team_score(match.team1)
						self._update_team_score(match.team2)
						self._update_group_ranking(match.group)
						if match.round == '3':
							# update next round (round of 16) if whole group is played
							self._update_round_of_16(match.group)
					else:
						#TODO during knockout phase, every match result provides one team for a future match
						pass
					# Update all bets for this match
					self._update_bets_score(match)

					# Update score of all betters
					self._update_users_score()

			req.context['result'] = match
		else:
			resp.status = falcon.HTTP_NOT_FOUND

	def _update_match_score(self, match):
		# type: (DBMatch) -> None
		if match.result:
			result = RESULT_PATTERN.match(match.result)
			goals1 = int(result.group(1))
			goals2 = int(result.group(2))
			if goals1 > goals2:
				match.winner = match.team1
			elif goals1 < goals2:
				match.winner = match.team2
			else:
				match.winner = None
			match.goals1 = goals1
			match.goals2 = goals2

	def _update_team_score(self, team):
		# type: (DBTeam) -> None
		team_id = team.id
		matches = self.session().query(DBMatch).\
			filter(DBMatch.round.in_(['1', '2', '3'])).\
			filter(DBMatch.result != None).\
			filter(or_(
				DBMatch.team1_id == team_id, 
				DBMatch.team2_id == team_id)).all()
		team.played = len(matches)
		team.won = len([match for match in matches if match.winner_id == team_id])
		team.drawn = len([match for match in matches if match.winner_id is None])
		team.lost = team.played - team.won - team.drawn
		goals_for_against = [(match.goals1, match.goals2) for match in matches if match.team1_id == team_id] + \
			[(match.goals2, match.goals1) for match in matches if match.team2_id == team_id]
		team.goals_for = sum(goals[0] for goals in goals_for_against)
		team.goals_against = sum(goals[1] for goals in goals_for_against)
		team.goals_diff = team.goals_for - team.goals_against
		team.points = 3 * team.won + team.drawn
		self.session().add(team)
		self.session().commit()
		self.session().refresh(team)

	def _update_group_ranking(self, group):
		teams = self.session().query(DBTeam).filter_by(group = group).\
			order_by(	DBTeam.points.desc(), \
						DBTeam.goals_diff.desc(), \
						DBTeam.goals_for.desc()).all()
		rank = 1
		points = goals_diff = goals_for = -100
		for team in teams:
			logger.debug('Group "%s": team %s' % (group, str(team)))
			team.rank = rank
			#TODO if several teams have the same rank then the next rank should be more than rank+1, e.g. 1,1,3,4
			if	team.points != points \
				or team.goals_diff != goals_diff or team.goals_for != goals_for:
				rank = rank + 1
				points = team.points
				goals_diff = team.goals_diff
				goals_for = team.goals_for
			self.session().add(team)
			self.session().commit()
			self.session().refresh(team)

	def _update_round_of_16(self, group):
		# first check if all matches in group have been played already
		unplayed = self.session().query(func.count('*')).select_from(DBMatch). \
			filter_by(group = group, result = None).scalar()
		if unplayed:
			return
		# all matches have been played, now check all teams from the group are uniquely ranked
		# (1 in rank 1, 1 in rank 2)
		teams = self.session().query(DBTeam).filter_by(group = group).all()
		rank1 = [team for team in teams if team.rank == 1]
		if len(rank1) == 1:
			# Find the next match for this result
			self._update_match_team('Winner %s' % group, rank1[0])
			rank2 = [team for team in teams if team.rank == 2]
			if len(rank2) == 1:
				# Find the next match for this result
				self._update_match_team('Runner-up %s' % group, rank2[0])
		#TODO if ranking not unique, record an action for administrator

	def _update_bets_score(self, match):
		# type (DBMatch) -> none
		# massage result for later queries
		result = match.result
		goals_diff = match.goals1 - match.goals2
		if goals_diff > 0:
			winner = 1
		elif goals_diff < 0:
			winner = 2
		else:
			winner = 0
		goals_diff = abs(goals_diff)
		# batch update of all bets for this match
		bets = inspect(DBBet).local_table
		connection = self.session().connection()
		# Perform updates for exact results (score 3)
		update = bets.update().where(bets.c.match_id == match.id).\
			where(bets.c.result == result).\
			values(score = 3)
		connection.execute(update)
		# Perform updates for correct results with same goals difference (score 2)
		update = bets.update().where(bets.c.match_id == match.id).\
			where(bets.c.result != result).\
			where(bets.c.winner == winner).\
			where(bets.c.goals_diff == goals_diff).\
			values(score = 2)
		connection.execute(update)
		# Perform updates for correct bet on winner (score 1)
		update = bets.update().where(bets.c.match_id == match.id).\
			where(bets.c.winner == winner).\
			where(bets.c.goals_diff != goals_diff).\
			values(score = 1)
		connection.execute(update)
		# Perform updates for lost bets (score 0)
		update = bets.update().where(bets.c.match_id == match.id).\
			where(bets.c.result is not None).\
			where(bets.c.winner != winner).\
			values(score = 0)
		connection.execute(update)

	def _update_users_score(self):
		#TODO limit update to users with bets for the current updated match (other users shall not change)
		# batch update of all users 
		bets = inspect(DBBet).local_table
		users = inspect(DBUser).local_table
		connection = self.session().connection()
		select_score = select([func.sum(bets.c.score)]).\
			where(bets.c.better_id == users.c.id).\
			where(bets.c.score != None)
		# this may lead to None instead of 0 if there are no bets with a valid score
		update = users.update().values(score = select_score)
		connection.execute(update)

	def _update_match_team(self, old_team_name, new_team):
		team_id = self.session().query(DBTeam.id).filter_by(name = old_team_name).scalar()
		match = self.session().query(DBMatch).filter(DBMatch.team1_id == team_id).one_or_none()
		if match:
			match.team1 = new_team
		else:
			match = self.session().query(DBMatch).filter(DBMatch.team2_id == team_id).one_or_none()
			match.team2 = new_team
		self.session().add(match)
		self.session().commit()
		self.session().refresh(match)
