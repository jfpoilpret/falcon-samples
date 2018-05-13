from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base  = declarative_base()

# Declare Team entity
class DBTeam(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key = True)
    name = Column(String)

    def __repr__(self):
        return 'Team(id = %d, name = %s)' % (self.id, self.name)

# Utility methods to create/drop DB schema from ORM mappings
def create_db(engine):
    metadata = DBTeam.metadata
    metadata.bind = engine
    metadata.create_all()

def drop_db(engine):
    metadata = DBTeam.metadata
    metadata.bind = engine
    metadata.drop_all()
