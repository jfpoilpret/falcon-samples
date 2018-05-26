import logging
import os
from sqlalchemy import create_engine

from .utils.sqlalchemy_util import SqlAlchemy
from .model import create_db, drop_db
from .utils.auth import Authenticator
from .initdb import init_db
from .configuration import Configuration

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
#logging.basicConfig(filename = config.log_output, level = config.log_level)
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
basedir = os.path.abspath(os.path.dirname(__file__))
#database = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
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

# Create basic authenticator for use with all Auth backend
authenticator = Authenticator(sql_middleware)
