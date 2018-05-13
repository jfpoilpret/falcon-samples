import os
from falcon import API
from falcon_marshmallow import Marshmallow
from sqlalchemy import create_engine

from .sqlalchemy import SqlAlchemy
from .model import create_db
from .team import Team, Teams

# Create SQLAlchemy engine
basedir = os.path.abspath(os.path.dirname(__file__))
database = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
engine = create_engine(database)
sql_middleware = SqlAlchemy(engine)

# Create DB if not exists
create_db(engine)

# Create Falcon API with proper middleware: Marshmallow (validation), SQLAlchemy (persistence)
api = application = API(middleware=[Marshmallow(), sql_middleware])

api.add_route('/team', Teams())
api.add_route('/team/{id:int}', Team())
