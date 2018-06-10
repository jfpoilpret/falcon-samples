from datetime import timedelta
import falcon
from marshmallow import Schema, fields
from ..utils import StrictSchema, TimeBase
from .resource import Resource

class TimeSchema(StrictSchema):
	delta = fields.TimeDelta()
	now = fields.DateTime()

class Time(Resource):
	schema = TimeSchema()

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		Resource.__init__(self, timebase)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		self._set_result(req)

	def on_delete(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		# check admin only
		self.check_admin(req)
		self.timebase().reset()

	def on_patch(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		# check admin only
		self.check_admin(req)
		values = req.context['json']
		if 'now' in values.keys():
			self.timebase().set_timebase(values['now'])
		elif 'delta' in values.keys():
			self.timebase().set_timedelta(values['delta'])
		self._set_result(req)

	def _set_result(self, req):
		# type: (falcon.Request) -> None
		req.context['result'] = {
			'now': self.now(),
			'delta': self.timebase().delta()
		}
