import os
import falcon
from falcon import API, HTTPError
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError, IntegrityError

from falcon_marshmallow import Marshmallow
from .marshmallow_util import context_middleware
from .falcon_util import ExceptionHandler
from .sqlalchemy import SqlAlchemy
from .model import create_db, drop_db

from .team import Team, Teams
from .venue import Venue, Venues
from .match import Match, Matches
from .user import User, Users

from .initdb import init_db

# Create SQLAlchemy engine
basedir = os.path.abspath(os.path.dirname(__file__))
database = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
engine = create_engine(database)
sql_middleware = SqlAlchemy(engine)

# Create DB if not exists
#TODO later make it configurable (command line args)
drop_db(engine)
create_db(engine)
init_db(sql_middleware.new_session())
sql_middleware.delete_session()

# Create Falcon API with proper middleware: Marshmallow (validation), SQLAlchemy (persistence)
api = application = API(middleware=[sql_middleware, context_middleware, Marshmallow()])

api.add_error_handler(Exception, ExceptionHandler(falcon.HTTP_INTERNAL_SERVER_ERROR, "Internal error"))
api.add_error_handler(DBAPIError, ExceptionHandler(falcon.HTTP_INTERNAL_SERVER_ERROR, "Database error"))
api.add_error_handler(IntegrityError, ExceptionHandler(falcon.HTTP_UNPROCESSABLE_ENTITY, "Integrity constraint error"))
# We have to re-register the following handlers because although registered by default, 
# they will never get called due to our Exception handler
api.add_error_handler(falcon.HTTPError, api._http_error_handler)
api.add_error_handler(falcon.HTTPStatus, api._http_status_handler)

api.add_route('/team', Teams())
api.add_route('/team/{id:int}', Team())
api.add_route('/venue', Venues())
api.add_route('/venue/{id:int}', Venue())
api.add_route('/match', Matches())
api.add_route('/match/{id:int}', Match())
api.add_route('/user', Users())
api.add_route('/user/{id_or_name}', User())
