from datetime import datetime
import falcon
from sqlalchemy.orm.session import Session
from ..utils import TimeBase
from ..model import DBUser

class Resource(object):
	def __init__(self, timebase = None):
		# type: (TimeBase) -> None
		self._timebase = timebase

	def timebase(self):
		# type: () -> TimeBase
		return self._timebase

	def now(self):
		# type: () -> datetime
		return self.timebase().now()

	def session(self):
		# type: () -> Session
		return self._session
	
	def result(self, req, resp, value):
		# type: (falcon.Request, falcon.Response, object) -> object
		if value is not None:
			req.context['result'] = value
		else:
			resp.status = falcon.HTTP_NOT_FOUND
		return value

	def is_admin(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> bool
		admin = req.context['user'].admin
		if not admin:
			resp.status = falcon.HTTP_FORBIDDEN
		return admin

	def get_user(self, id_or_name):
		# type: (str) -> DBUser
		if id_or_name.isnumeric():
			return self.session().query(DBUser).filter_by(id = int(id_or_name)).one_or_none()
		else:
			return self.session().query(DBUser).filter_by(login = id_or_name).one_or_none()
