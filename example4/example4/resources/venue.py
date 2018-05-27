import falcon
from marshmallow import fields, Schema

from .utils.marshmallow_util import URLFor
from .model import DBVenue

class VenueSchema(Schema):
	id = fields.Integer()
	href = URLFor('/venue/{id}')
	name = fields.String(required=True)

class Venues(object):
	schema = VenueSchema(many = True)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self._session.query(DBVenue).all()

class Venue(object):
	schema = VenueSchema()

	def on_get(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		Venue = self._session.query(DBVenue).filter_by(id = id).one_or_none()
		if Venue:
			req.context['result'] = Venue
		else:
			resp.status = falcon.HTTP_NOT_FOUND
