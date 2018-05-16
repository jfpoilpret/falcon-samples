import falcon
from marshmallow import fields, Schema

from .model import DBVenue

class VenueSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

class Venues(object):
    schema = VenueSchema(many = True)

    def on_get(self, req, resp):
        req.context['result'] = self._session.query(DBVenue).all()

class Venue(object):
    schema = VenueSchema()

    def on_get(self, req, resp, id):
        Venue = self._session.query(DBVenue).filter_by(id = id).one_or_none()
        if Venue:
            req.context['result'] = Venue
        else:
            resp.status = falcon.HTTP_NOT_FOUND
