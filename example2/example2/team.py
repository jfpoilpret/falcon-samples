import falcon
from marshmallow import fields, Schema

from .storage import Storage

class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

class Team(object):
    get_schema = TeamSchema(many = True)
    schema = TeamSchema()

    def __init__(self, storage):
        self._storage = storage

    def on_get(self, req, resp):
        req.context['result'] = self._storage.teams()

    def on_post(self, req, resp):
        req.context['result'] = self._storage.add_team(req.context['json'])
        resp.status = falcon.HTTP_CREATED
