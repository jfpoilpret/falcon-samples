from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base  = declarative_base()

#TODO Add other fields (flag, jersey, location...)
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
        return 'Match(id = %d, date = %s, venue = %s, team1 = %s, team2 = %s, result = %s)' % 
            (self.id, self.matchtime.strftime('%d.%m.%Y %H:%M'), self.venue.name if self.venue else "unknown",
            self.team1.name if self.team1 else 'unknown', self.team2.name if self.team2 else 'unknown',
            self.result or 'unknown')

# Utility methods to create/drop DB schema from ORM mappings
def create_db(engine):
    metadata = DBTeam.metadata
    metadata.bind = engine
    metadata.create_all()

def drop_db(engine):
    metadata = DBTeam.metadata
    metadata.bind = engine
    metadata.drop_all()
