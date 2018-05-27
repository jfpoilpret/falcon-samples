from datetime import timedelta
import falcon
from marshmallow import Schema, fields
from ..utils.marshmallow_util import StrictSchema
from ..utils.timebase import TimeBase

class TimeSchema(StrictSchema):
	delta = fields.Integer()
	now = fields.DateTime()

class Time(object):
	schema = TimeSchema()

	def __init__(self, timebase):
		# type: (TimeBase) -> None
		self._timebase = timebase

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = {
			'now': self._timebase.now(),
			'delta': self._timebase.delta().total_seconds()
		}

	def on_delete(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		# check admin only
		if not req.context['user'].admin:
			resp.status = falcon.HTTP_FORBIDDEN
			return
		self._timebase.reset()

	def on_patch(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		# check admin only
		if not req.context['user'].admin:
			resp.status = falcon.HTTP_FORBIDDEN
			return
		values = req.context['json']
		if 'now' in values.keys():
			self._timebase.set_timebase(values['now'])
		elif 'delta' in values.keys():
			delta = timedelta(seconds = values['delta'])
			self._timebase.set_timedelta(delta)
