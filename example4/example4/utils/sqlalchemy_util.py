import logging
from sqlalchemy import event, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

logger = logging.getLogger(__name__)

class SqlAlchemy(object):
	def __init__(self, engine):
		factory = sessionmaker(bind = engine)
		self._session_holder = scoped_session(factory)
    
	def new_session(self):
		# type: () -> Session
		return self._session_holder()

	def delete_session(self):
		self._session_holder.remove()

	def process_resource(self, req, resp, resource, params):
		resource._session = self.new_session()

	def process_response(self, req, resp, resource, req_succeeded):
		if req_succeeded:
			resource._session.commit()
		self.delete_session()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()
    
def debug_object_state(entity, msg):
	inspector = inspect(entity)
	if inspector.transient:
		state = 'transient'
	elif inspector.pending:
		state = 'pending'
	elif inspector.persistent:
		state = 'persistent'
	elif inspector.deleted:
		state = 'deleted'
	elif inspector.detached:
		state = 'detached'
	else:
		state = 'unknown'
	logger.debug('Object state: %s %s', msg, state)
