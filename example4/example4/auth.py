from uuid import uuid4
from datetime import datetime, timedelta
from .model import DBUser

class Authenticator(object):
	def __init__(self, sql_middleware, duration = 86400, reconduct = False):
		self._sql_middleware = sql_middleware
		self._duration = timedelta(seconds = duration)
		self._reconduct = reconduct
		self._tokens = {}
	
	def new_token(self, user):
		token = uuid4()
		expiry = datetime.now() + self._duration
		self._tokens[token] = (user.id, expiry)
		return token, expiry

	def remove_token(self, token):
		if token in self._tokens:
			del self._tokens[token]

	def expire_tokens(self):
		now = datetime.now()
		expired = []
		for token, (id, expiry) in self._tokens.items():
			if expiry < now:
				expired.append(token)
		for token in expired:
			del self._tokens[token]

	def __call__(self, token):
		if token in self._tokens:
			id, expiry = self._tokens[token]
			if expiry > datetime.now():
				# Update expiry date further if needed?
				if self._reconduct:
					self._tokens[token] = (id, datetime.now() + self._duration)
				try:
					session = self._sql_middleware.new_session()
					user = session.query(DBUser).filter_by(id = id).one_or_none()
					if user:
						# log last connection time
						user.connection = datetime.now()
						session.add(user)
						session.commit()
						return user
				finally:
					self._sql_middleware.delete_session()
			else:
				self.remove_token(token)
		#TODO log failed connection?
		return None

	def __call__(self, username, password):
		try:
			session = self._sql_middleware.new_session()
			user = session.query(DBUser).filter_by(login = username).one_or_none()
			#TODO hash password to compare
			if user and user.password == password:
				# log last connection time
				user.connection = datetime.now()
				session.add(user)
				session.commit()
				return user
			#TODO log bad connection
			return None
		finally:
			self._sql_middleware.delete_session()
