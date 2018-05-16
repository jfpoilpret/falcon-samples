import os
from falcon import API
from falcon_marshmallow import Marshmallow
from sqlalchemy import create_engine

from .sqlalchemy import SqlAlchemy
from .model import create_db, drop_db
from .team import Team, Teams
from .venue import Venue, Venues
from .match import Match, Matches
from .initdb import init_db

# Create SQLAlchemy engine
basedir = os.path.abspath(os.path.dirname(__file__))
database = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
engine = create_engine(database)
sql_middleware = SqlAlchemy(engine)

# Create DB if not exists
drop_db(engine)
create_db(engine)
init_db(sql_middleware.new_session())
sql_middleware.delete_session()

# Create Falcon API with proper middleware: Marshmallow (validation), SQLAlchemy (persistence)
api = application = API(middleware=[sql_middleware, Marshmallow()])

api.add_route('/team', Teams())
api.add_route('/team/{id:int}', Team())
api.add_route('/venue', Venues())
api.add_route('/venue/{id:int}', Venue())
api.add_route('/match', Matches())
api.add_route('/match/{id:int}', Match())
