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

	def __repr__(self):
		return 'Team(id = %d, name = %s, group = %s)' % (self.id, self.name, self.group)

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
	group = Column(String)

	venue = relationship(DBVenue)
	team1 = relationship(DBTeam, foreign_keys = [team1_id])
	team2 = relationship(DBTeam, foreign_keys = [team2_id])

	result = Column(String)

	def __repr__(self):
		return 'Match(id = %d, date = %s, venue = %s (%d), team1 = %s (%d), team2 = %s (%d), result = %s)' % (
			self.id, self.matchtime.strftime('%d.%m.%Y %H:%M'), self.venue.name if self.venue else "unknown", self.venue_id,
			self.team1.name if self.team1 else 'unknown', self.team1_id, self.team2.name if self.team2 else 'unknown', self.team2_id,
			self.result or 'unknown')

#TODO Add picture or gravatar?
class DBUser(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	login = Column(String, nullable = False, unique = True)
	#TODO Change to binary (hashed)?
	password = Column(String, nullable = False)
	status = Column(Enum('pending', 'approved', 'suspended'))
	admin = Column(Boolean, nullable = False, default = False)
	fullname = Column(String, nullable = False, unique = True)
	email = Column(String, unique = True)
	creation = Column(DateTime, nullable = False)
	connection = Column(DateTime)

	def __repr__(self):
		return 'User(id = %d, login = %s, fullname = %s, status = %s, admin = %s, creation = %s, connection = %s)' % (
			self.id, self.login, self.fullname, self.status, str(self.admin), 
			self.creation.strftime('%d.%m.%Y %H:%M'), self.connection.strftime('%d.%m.%Y %H:%M'))

# Utility methods to create/drop DB schema from ORM mappings
def create_db(engine):
	metadata = DBTeam.metadata
	metadata.bind = engine
	metadata.create_all()

def drop_db(engine):
	metadata = DBTeam.metadata
	metadata.bind = engine
	metadata.drop_all()
