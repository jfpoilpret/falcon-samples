import logging
import os

import falcon
from falcon import API, HTTPError
from falcon_auth import FalconAuthMiddleware, TokenAuthBackend
from falcon_marshmallow import Marshmallow

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError, IntegrityError

from .model import create_db, drop_db

from .utils.falcon_util import ExceptionHandler, LoggingMiddleware
from .utils.marshmallow_util import context_middleware
from .utils.sqlalchemy_util import SqlAlchemy
from .utils.timebase import TimeBase
from .utils.auth import Authenticator

from .initdb import init_db
from .configuration import Configuration

def create_app():
	# Get configuration
	config = Configuration()

	logging_args = {
		'level': config.log_level
	}
	if config.log_output:
		logging_args['filename'] = config.log_output
	if config.log_format:
		logging_args['format'] = config.log_format
	if config.log_style:
		logging_args['style'] = config.log_style
	if config.log_dateformat:
		logging_args['datefmt'] = config.log_dateformat

	logging.basicConfig(**logging_args)
	logger = logging.getLogger(__name__)

	# Create SQLAlchemy engine
	basedir = os.path.abspath(os.path.dirname(__file__))
	database = '%s:///%s' % (config.db_type, os.path.join(basedir, config.db_name))
	engine = create_engine(database)
	sql_middleware = SqlAlchemy(engine)

	# Create DB if required
	#TODO make it smarter: drop if required (DEV, TEST, TRAIN...), create and init if not exists
	if config.drop_db:
		logger.debug('Dropping current DB...')
		drop_db(engine)
		logger.debug('Current DB dropped. Recreating new DB...')
		create_db(engine)
		logger.debug('New DB recreated. Initializing DB content.')
		init_db(sql_middleware.new_session())
		logger.debug('DB content initialized.')
		sql_middleware.delete_session()

	# Create TimeBase service
	timebase = TimeBase()
	# Create basic authenticator for use with all Auth backend
	authenticator = Authenticator(timebase, sql_middleware)

	# Create default Token Auth backend
	backend = TokenAuthBackend(authenticator)

	# Create Falcon API with proper middleware: Marshmallow (validation), SQLAlchemy (persistence)
	api = API(middleware=[LoggingMiddleware(), sql_middleware, FalconAuthMiddleware(backend), context_middleware, Marshmallow()])

	api.add_error_handler(Exception, ExceptionHandler(falcon.HTTP_INTERNAL_SERVER_ERROR, "Internal error"))
	api.add_error_handler(DBAPIError, ExceptionHandler(falcon.HTTP_INTERNAL_SERVER_ERROR, "Database error"))
	api.add_error_handler(IntegrityError, ExceptionHandler(falcon.HTTP_UNPROCESSABLE_ENTITY, "Integrity constraint error"))
	# We have to re-register the following handlers because although registered by default, 
	# they will never get called due to our Exception handler
	api.add_error_handler(falcon.HTTPError, api._http_error_handler)
	api.add_error_handler(falcon.HTTPStatus, api._http_status_handler)

	from .resources import Team, Teams, Venue, Venues, Match, Matches, Bets, User, Users, Token, Time

	if config.timebase_changes:
		api.add_route('/time', Time(timebase))
	api.add_route('/token', Token())
	api.add_route('/team', Teams())
	api.add_route('/team/{id:int}', Team())
	api.add_route('/venue', Venues())
	api.add_route('/venue/{id:int}', Venue())
	api.add_route('/match', Matches())
	api.add_route('/match/{id:int}', Match(timebase))
	api.add_route('/user', Users(timebase))
	api.add_route('/user/{id_or_name}', User())
	api.add_route('/bet', Bets(timebase))

	logger.info('API service started.')
	
	return api
