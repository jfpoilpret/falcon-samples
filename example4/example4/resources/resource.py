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
	
	def check_result(self, item_name, value):
		# type: (str, object) -> object
		if value is None:
			raise falcon.HTTPNotFound(description = 'This %s does not exist' % item_name)
		return value

	def check_and_set_result(self, req, item_name, value):
		# type: (falcon.Request, str, object) -> object
		value = self.check_result(item_name, value)
		req.context['result'] = value
		return value

	def is_admin(self, req):
		# type: (falcon.Request) -> bool
		return req.context['user'].admin

	def check_admin(self, req):
		# type: (falcon.Request) -> None
		if not req.context['user'].admin:
			raise falcon.HTTPForbidden(description = 'Only an administrator can perform this action.')

	def get_user(self, id_or_name):
		# type: (str) -> DBUser
		if id_or_name.isnumeric():
			return self.session().query(DBUser).filter_by(id = int(id_or_name)).one_or_none()
		else:
			return self.session().query(DBUser).filter_by(email = id_or_name).one_or_none()
