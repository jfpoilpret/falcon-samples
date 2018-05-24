import os
from sqlalchemy import create_engine

from .utils.sqlalchemy_util import SqlAlchemy
from .model import create_db, drop_db
from .utils.auth import Authenticator
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

# Create basic authenticator for use with all Auth backend
authenticator = Authenticator(sql_middleware)
