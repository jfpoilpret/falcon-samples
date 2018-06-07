import falcon
from marshmallow import fields, Schema

from ..utils import URLFor
# from ..utils.marshmallow_util import URLFor
from .resource import Resource
from ..model import DBVenue

class VenueSchema(Schema):
	id = fields.Integer()
	href = URLFor('/venue/{id}')
	name = fields.String(required=True)

class Venues(Resource):
	schema = VenueSchema(many = True)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self.session().query(DBVenue).all()

class Venue(Resource):
	schema = VenueSchema()

	def on_get(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		self.result(req, resp, self.session().query(DBVenue).filter_by(id = id).one_or_none())
