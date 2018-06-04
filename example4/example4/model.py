from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, Enum, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base  = declarative_base()

#TODO Add other fields (flag, jersey, team, base camp location...)
#TODO review field attributes (size, unicity...)
#TODO shall we define "virtual" teams, like "Group A Winner" to be used for 2nd round matches (16th finals...)?
# Declare Team entity
class DBTeam(Base):
	__tablename__ = 'team'

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False, unique = True)
	group = Column(String, nullable = False)

	rank = Column(Integer)
	played = Column(Integer, nullable = False, default = 0)
	won = Column(Integer, nullable = False, default = 0)
	drawn = Column(Integer, nullable = False, default = 0)
	lost = Column(Integer, nullable = False, default = 0)
	goals_for = Column(Integer, nullable = False, default = 0)
	goals_against = Column(Integer, nullable = False, default = 0)
	goals_diff = Column(Integer, nullable = False, default = 0)
	points = Column(Integer, nullable = False, default = 0)

	def __repr__(self):
		return 'Team(id = %d, name = %s, group = %s, points = %d)' % (self.id, self.name, self.group, self.points)

#TODO Add picture, TZ, coordinates?
class DBVenue(Base):
	__tablename__ = 'venue'

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False, unique = True)

	def __repr__(self):
		return 'Venue(id = %d, name = %s)' % (self.id, self.name)

class DBMatch(Base):
	__tablename__ = 'match'

	id = Column(Integer, primary_key = True)
	round = Column(String, nullable = False)
	matchtime = Column(DateTime, nullable = False)
	venue_id = Column(Integer, ForeignKey('venue.id'), nullable = False)
	team1_id = Column(Integer, ForeignKey('team.id'))
	team2_id = Column(Integer, ForeignKey('team.id'))
	winner_id = Column(Integer, ForeignKey('team.id'))
	group = Column(String)

	venue = relationship(DBVenue)
	team1 = relationship(DBTeam, foreign_keys = [team1_id])
	team2 = relationship(DBTeam, foreign_keys = [team2_id])

	result = Column(String)
	winner = relationship(DBTeam, foreign_keys = [winner_id])
	goals1 = Column(Integer)
	goals2 = Column(Integer)

	def __repr__(self):
		return 'Match(id = %d, date = %s, venue = %s (%d), team1 = %s (%d), team2 = %s (%d), result = %s)' % (
			self.id, self.matchtime.strftime('%d.%m.%Y %H:%M'), self.venue.name if self.venue else "unknown", self.venue_id,
			self.team1.name if self.team1 else 'unknown', self.team1_id, self.team2.name if self.team2 else 'unknown', self.team2_id,
			self.result or 'unknown')

#TODO make email the login? more logical!
#TODO Add picture or gravatar?
class DBUser(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	login = Column(String, nullable = False, unique = True)
	password = Column(String, nullable = False)
	status = Column(Enum('pending', 'approved', 'suspended'))
	admin = Column(Boolean, nullable = False, default = False)
	fullname = Column(String, nullable = False, unique = True)
	email = Column(String, unique = True)
	score = Column(Integer, default = 0)
	creation = Column(DateTime, nullable = False)
	connection = Column(DateTime)

	def __repr__(self):
		return 'User(id = %d, login = %s, fullname = %s, status = %s, admin = %s, creation = %s, connection = %s)' % (
			self.id, self.login, self.fullname, self.status, str(self.admin), 
			self.creation.strftime('%d.%m.%Y %H:%M'), self.connection.strftime('%d.%m.%Y %H:%M'))

#TODO unique key on better+match
class DBBet(Base):
	__tablename__ = 'bet'

	id = Column(Integer, primary_key = True)
	bettime = Column(DateTime)
	better_id = Column(Integer, ForeignKey('user.id'), nullable = False)
	match_id = Column(Integer, ForeignKey('match.id'), nullable = False)

	better = relationship(DBUser)
	match = relationship(DBMatch)

	result = Column(String)
	# The 3 next columns are internal ony, they are here to accelerate computation of user's score
	# winner is either:
	#	1 if result claims team1 is gonna win
	#	2 if result claims team2 is gonna win
	#	0 if result claims this will be a draw
	#	None if result is None
	winner = Column(Integer)
	# goals_diff is the goal difference between winner and loser in result (always 0 for a draw)
	goals_diff = Column(Integer)
	# score indicates the amount scored by better on this single bet:
	#	3 if result matches exact match result
	#	2 if result matches winner and goals difference
	#	1 if result matches winner
	#	0 if result is wrong
	#	None if result is None
	score = Column(Integer)

	def __repr__(self):
		return 'Bet(id = %d, date = %s, user = %s (%d), match = %s-%s (%d), result = %s)' % (
			self.id, self.bettime.strftime('%d.%m.%Y %H:%M'), self.user.login, self.better_id,
			self.match.team1.name, self.match.team2.name, self.result or 'unknown')
	
# Utility methods to create/drop DB schema from ORM mappings
def create_db(engine):
	metadata = DBTeam.metadata
	metadata.bind = engine
	metadata.create_all()

def drop_db(engine):
	metadata = DBTeam.metadata
	metadata.bind = engine
	metadata.drop_all()
