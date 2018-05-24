from uuid import uuid4
from datetime import datetime, timedelta
from ..model import DBUser

class Authenticator(object):
	instance = None

	def __init__(self, sql_middleware, duration = 86400, reconduct = False):
		self._sql_middleware = sql_middleware
		self._duration = timedelta(seconds = duration)
		self._reconduct = reconduct
		self._tokens = {}
		Authenticator.instance = self
	
	def new_token(self, user):
		token = uuid4()
		expiry = datetime.now() + self._duration
		self._tokens[str(token)] = (user.id, expiry)
		print('Authenticator.new_token()' + str(token))
		return token, expiry

	def remove_token(self, token):
		if token in self._tokens.keys():
			del self._tokens[token]

	def expire_tokens(self):
		now = datetime.now()
		expired = []
		for token, (id, expiry) in self._tokens.items():
			if expiry < now:
				expired.append(token)
		for token in expired:
			del self._tokens[token]

	def authenticate_token(self, token):
		print('Authenticator.__call__(token) #1')
		print(token)
		if token in self._tokens.keys():
			print('Authenticator.__call__(token) #2')
			id, expiry = self._tokens[token]
			print('Authenticator.__call__(token) #3')
			if expiry > datetime.now():
				print('Authenticator.__call__(token) #4')
				# Update expiry date further if needed?
				if self._reconduct:
					print('Authenticator.__call__(token) #5')
					self._tokens[token] = (id, datetime.now() + self._duration)
				try:
					print('Authenticator.__call__(token) #6')
					session = self._sql_middleware.new_session()
					print('Authenticator.__call__(token) #7')
					user = session.query(DBUser).filter_by(id = id).one_or_none()
					print('Authenticator.__call__(token) #8')
					if user:
						print('Authenticator.__call__(token) #9')
						# log last connection time
						# user.connection = datetime.now()
						# session.add(user)
						# session.commit()
						return user
				finally:
					pass
					# self._sql_middleware.delete_session()
			else:
				print('Authenticator.__call__(token) #10')
				self.remove_token(token)
		print('Authenticator.__call__(token) #11')
		#TODO log failed connection?
		return None

	def authenticate_user_password(self, username, password):
		try:
			print('Authenticator.__call__(user, password) #1')
			session = self._sql_middleware.new_session()
			print('Authenticator.__call__(user, password) #2')
			user = session.query(DBUser).filter_by(login = username).one_or_none()
			print('Authenticator.__call__(user, password) #3')
			#TODO hash password to compare
			if user and user.password == password:
				print('Authenticator.__call__(user, password) #4.1')
				# log last connection time
				# user.connection = datetime.now()
				# session.add(user)
				# session.commit()
				return user
			#TODO log bad connection
			print('Authenticator.__call__(user, password) #4.2')
			return None
		finally:
			pass
			# self._sql_middleware.delete_session()

	def __call__(self, username_or_token, password = None):
		if password:
			return self.authenticate_user_password(username_or_token, password)
		else:
			return self.authenticate_token(username_or_token)
