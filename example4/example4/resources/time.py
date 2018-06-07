from datetime import timedelta
import falcon
from marshmallow import Schema, fields
from ..utils.marshmallow_util import StrictSchema
from ..utils.timebase import TimeBase
from .resource import Resource

class TimeSchema(StrictSchema):
	delta = fields.Integer()
	now = fields.DateTime()

class Time(Resource):
	schema = TimeSchema()

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		Resource.__init__(self, timebase)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = {
			'now': self.now(),
			'delta': self.timebase().delta().total_seconds()
		}

	def on_delete(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		# check admin only
		if not self.is_admin(req, resp):
			return
		self.timebase().reset()

	def on_patch(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		# check admin only
		if not self.is_admin(req, resp):
			return
		values = req.context['json']
		if 'now' in values.keys():
			self.timebase().set_timebase(values['now'])
		elif 'delta' in values.keys():
			delta = timedelta(seconds = values['delta'])
			self.timebase().set_timedelta(delta)
