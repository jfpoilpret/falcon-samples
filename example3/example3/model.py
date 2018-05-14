from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base  = declarative_base()

#TODO Add group and other fields (flag, jersey...)
#TODO review field attributes (size, unicity...)
# Declare Team entity
class DBTeam(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    group = Column(String)

    def __repr__(self):
        return 'Team(id = %d, name = %s, group = %s)' % (self.id, self.name, self.group)

# Utility methods to create/drop DB schema from ORM mappings
def create_db(engine):
    metadata = DBTeam.metadata
    metadata.bind = engine
    metadata.create_all()

def drop_db(engine):
    metadata = DBTeam.metadata
    metadata.bind = engine
    metadata.drop_all()
