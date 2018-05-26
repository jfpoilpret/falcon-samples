import logging
from uuid import uuid4
from datetime import datetime, timedelta
from .sqlalchemy_util import SqlAlchemy
from ..model import DBUser

logger = logging.getLogger(__name__)

class Authenticator(object):
	instance = None

	def __init__(self, sql_middleware, duration = 86400, reconduct = False):
		# type: (SqlAlchemy, int, bool) -> None
		self._sql_middleware = sql_middleware
		self._duration = timedelta(seconds = duration)
		self._reconduct = reconduct
		self._tokens = {}
		Authenticator.instance = self
	
	def new_token(self, user):
		logger.debug('new_token(%s)', str(user))
		token = uuid4()
		expiry = datetime.now() + self._duration
		self._tokens[str(token)] = (user.id, expiry)
		return token, expiry

	def remove_token(self, token):
		logger.debug('remove_token(%s)', token)
		if token in self._tokens.keys():
			del self._tokens[token]

	def expire_tokens(self):
		logger.debug('expire_tokens()')
		now = datetime.now()
		expired = []
		for token, (id, expiry) in self._tokens.items():
			if expiry < now:
				expired.append(token)
		for token in expired:
			logger.debug('expire_tokens() removing token %s', token)
			del self._tokens[token]

	def authenticate_token(self, token):
		logger.debug('authenticate_token(%s)', token)
		if token in self._tokens.keys():
			logger.debug('token is in tokens list: %s', token)
			id, expiry = self._tokens[token]
			if expiry > datetime.now():
				logger.debug('token has not expired: %s', token)
				# Update expiry date further if needed?
				if self._reconduct:
					self._tokens[token] = (id, datetime.now() + self._duration)
				session = self._sql_middleware.new_session()
				user = session.query(DBUser).filter_by(id = id).one_or_none()
				if user:
					logger.debug('token %s is for user %s', token, str(user))
					# log last connection time
					user.connection = datetime.now()
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
		logger.debug('authenticate_user_password(%s)', username)
		session = self._sql_middleware.new_session()
		user = session.query(DBUser).filter_by(login = username).one_or_none()
		#TODO hash password to compare
		if user and user.password == password and user.status == 'approved':
			logger.debug('User %s successfully authenticated', username)
			# log last connection time
			user.connection = datetime.now()
			session.add(user)
			session.commit()
			session.refresh(user)
			session.expunge(user)
			return user
		# log bad connection
		logger.info('Could not authenticate username %s', username)
		return None

	def __call__(self, username_or_token, password = None):
		if password:
			return self.authenticate_user_password(username_or_token, password)
		else:
			return self.authenticate_token(username_or_token)
