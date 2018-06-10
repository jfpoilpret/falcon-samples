import logging
from uuid import uuid4
from hashlib import sha256
from datetime import datetime, timedelta
from .sqlalchemy_util import SqlAlchemy
from .timebase import TimeBase
from ..model import DBUser

logger = logging.getLogger(__name__)

# Got these 2 hash password functions from:
# https://www.pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
	# type: (str) -> str
	salt = uuid4().hex
	return sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def verify_password(expected, actual):
	# type: (str, str) -> bool
	password, salt = expected.split(':')
	return password == sha256(salt.encode() + actual.encode()).hexdigest()

class Authenticator(object):
	instance = None

	def __init__(self, timebase, sql_middleware, duration = 86400, reconduct = False):
		# type: (TimeBase, SqlAlchemy, int, bool) -> None
		self._timebase = timebase
		self._sql_middleware = sql_middleware
		self._duration = timedelta(seconds = duration)
		self._reconduct = reconduct
		self._tokens = {}
		Authenticator.instance = self
	
	def new_token(self, user):
		# type: (object) -> (UUID, datetime)
		logger.debug('new_token(%s)', str(user))
		token = uuid4()
		expiry = datetime.utcnow() + self._duration
		self._tokens[str(token)] = (user.id, expiry)
		return token, expiry

	def remove_token(self, token):
		# type: (str) -> None
		logger.debug('remove_token(%s)', token)
		if token in self._tokens.keys():
			del self._tokens[token]

	def expire_tokens(self):
		# type: () -> None
		logger.debug('expire_tokens()')
		now = datetime.utcnow()
		expired = []
		for token, (id, expiry) in self._tokens.items():
			if expiry < now:
				expired.append(token)
		for token in expired:
			logger.debug('expire_tokens() removing token %s', token)
			del self._tokens[token]

	def authenticate_token(self, token):
		# type: (str) -> DBUser
		logger.debug('authenticate_token(%s)', token)
		if token in self._tokens.keys():
			logger.debug('token is in tokens list: %s', token)
			id, expiry = self._tokens[token]
			if expiry > datetime.utcnow():
				logger.debug('token has not expired: %s', token)
				# Update expiry date further if needed?
				if self._reconduct:
					self._tokens[token] = (id, datetime.utcnow() + self._duration)
				session = self._sql_middleware.new_session()
				user = session.query(DBUser).filter_by(id = id).one_or_none()
				if user:
					logger.debug('token %s is for user %s', token, str(user))
					# log last connection time
					user.connection = self._timebase.now()
					session.add(user)
					session.commit()
					session.refresh(user)
					session.expunge(user)
					return user
				logger.debug('token has no associated user: %s', token)
			else:
				logger.debug('token has expired: %s', token)
			self.remove_token(token)
		# log failed connection
		logger.info('Could not authenticate token %s', token)
		return None

	def authenticate_user_password(self, username, password):
		# type: (str, str) -> DBUser
		logger.debug('authenticate_user_password(%s)', username)
		session = self._sql_middleware.new_session()
		user = session.query(DBUser).filter_by(email = username).one_or_none()
		if user and user.status == 'approved' and verify_password(user.password, password):
			logger.debug('User %s successfully authenticated', username)
			# log last connection time
			user.connection = self._timebase.now()
			session.add(user)
			session.commit()
			session.refresh(user)
			session.expunge(user)
			return user
		# log bad connection
		logger.info('Could not authenticate username %s', username)
		return None

	def __call__(self, username_or_token, password = None):
		# type: (str, str) -> DBUser
		if password:
			return self.authenticate_user_password(username_or_token, password)
		else:
			return self.authenticate_token(username_or_token)
