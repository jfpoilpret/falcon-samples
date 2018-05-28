import logging
import falcon
from falcon import API, HTTPError
from sqlalchemy.exc import DBAPIError, IntegrityError

from falcon_auth import FalconAuthMiddleware, TokenAuthBackend
from falcon_marshmallow import Marshmallow
from .utils.falcon_util import ExceptionHandler, LoggingMiddleware

from .utils.auth import Authenticator
from .utils.marshmallow_util import context_middleware
from .init_app import sql_middleware, config, timebase

from .resources.team import Team, Teams
from .resources.venue import Venue, Venues
from .resources.match import Match, Matches
from .resources.user import User, Users
from .resources.token import Token
from .resources.time import Time

# Create default Token Auth backend
backend = TokenAuthBackend(Authenticator.instance)

# Create Falcon API with proper middleware: Marshmallow (validation), SQLAlchemy (persistence)
api = application = API(middleware=[LoggingMiddleware(), sql_middleware, FalconAuthMiddleware(backend), context_middleware, Marshmallow()])

api.add_error_handler(Exception, ExceptionHandler(falcon.HTTP_INTERNAL_SERVER_ERROR, "Internal error"))
api.add_error_handler(DBAPIError, ExceptionHandler(falcon.HTTP_INTERNAL_SERVER_ERROR, "Database error"))
api.add_error_handler(IntegrityError, ExceptionHandler(falcon.HTTP_UNPROCESSABLE_ENTITY, "Integrity constraint error"))
# We have to re-register the following handlers because although registered by default, 
# they will never get called due to our Exception handler
api.add_error_handler(falcon.HTTPError, api._http_error_handler)
api.add_error_handler(falcon.HTTPStatus, api._http_status_handler)

if config.timebase_changes:
	api.add_route('/time', Time(timebase))
api.add_route('/token', Token())
api.add_route('/team', Teams())
api.add_route('/team/{id:int}', Team())
api.add_route('/venue', Venues())
api.add_route('/venue/{id:int}', Venue())
api.add_route('/match', Matches())
api.add_route('/match/{id:int}', Match())
api.add_route('/user', Users(timebase))
api.add_route('/user/{id_or_name}', User())

logging.getLogger(__name__).info('API service started.')
