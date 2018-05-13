import falcon
from marshmallow import fields, Schema

from .storage import Storage

class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

class Teams(object):
    get_schema = TeamSchema(many = True)
    schema = TeamSchema()

    def __init__(self, storage):
        self._storage = storage

    def on_get(self, req, resp):
        req.context['result'] = self._storage.teams()

    def on_post(self, req, resp):
        req.context['result'] = self._storage.add_team(req.context['json'])
        resp.status = falcon.HTTP_CREATED

class Team(object):
    schema = TeamSchema()

    def __init__(self, storage):
        self._storage = storage

    def on_get(self, req, resp, id):
        team = self._storage.team(id)
        if team:
            req.context['result'] = team
        else:
            resp.status = falcon.HTTP_NOT_FOUND

    def on_delete(self, req, resp, id):
        if not self._storage.remove_team(id):
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            resp.status = falcon.HTTP_NO_CONTENT

    #TODO put, patch
