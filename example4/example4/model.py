from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, Enum, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

Base  = declarative_base()

#TODO Add other fields (flag, jersey, team, base camp location...)
class DBTeam(Base):
	__tablename__ = 'team'

	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False, unique = True)
	group = Column(String(20), nullable = False)

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
	name = Column(String(100), nullable = False, unique = True)

	def __repr__(self):
		return 'Venue(id = %d, name = %s)' % (self.id, self.name)

class DBMatch(Base):
	__tablename__ = 'match'

	id = Column(Integer, primary_key = True)
	matchnumber = Column(Integer, nullable = False, unique = True)
	round = Column(String(50), nullable = False)
	matchtime = Column(DateTime, nullable = False)
	venue_id = Column(Integer, ForeignKey('venue.id'), nullable = False)
	team1_id = Column(Integer, ForeignKey('team.id'), nullable = False)
	team2_id = Column(Integer, ForeignKey('team.id'), nullable = False)
	winner_id = Column(Integer, ForeignKey('team.id'))
	group = Column(String(20))

	venue = relationship(DBVenue)
	team1 = relationship(DBTeam, foreign_keys = [team1_id])
	team2 = relationship(DBTeam, foreign_keys = [team2_id])

	result = Column(String(5))
	winner = relationship(DBTeam, foreign_keys = [winner_id])
	goals1 = Column(Integer)
	goals2 = Column(Integer)

	def __repr__(self):
		return 'Match(id = %d, date = %s, venue = %s (%d), team1 = %s (%d), team2 = %s (%d), result = %s)' % (
			self.id, self.matchtime.isoformat(), self.venue.name, self.venue_id,
			self.team1.name, self.team1_id, self.team2.name, self.team2_id,
			self.result or 'unknown')

#TODO Add picture or gravatar?
class DBUser(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	email = Column(String(100), nullable = False, unique = True)
	password = Column(String(250), nullable = False)
	status = Column(Enum('pending', 'approved', 'suspended'), nullable = False)
	admin = Column(Boolean, nullable = False, default = False)
	fullname = Column(String(100), nullable = False, unique = True)
	score = Column(Integer, default = 0)
	creation = Column(DateTime, nullable = False)
	connection = Column(DateTime)

	def __repr__(self):
		return 'User(id = %d, email = %s, fullname = %s, status = %s, admin = %s, creation = %s, connection = %s)' % (
			self.id, self.email, self.fullname, self.status, str(self.admin), 
			self.creation.isoformat(), 
			self.connection.isoformat() if self.connection else 'never')

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

	__table_args__ = (
		UniqueConstraint("better_id", "match_id"),
	)

	def __repr__(self):
		return 'Bet(id = %d, date = %s, user = %s (%d), match = %s-%s (%d), result = %s)' % (
			self.id, self.bettime.isoformat() if self.bettime else 'no bet', 
			self.better.email, self.better_id,
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
