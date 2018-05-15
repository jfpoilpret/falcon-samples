import falcon
from marshmallow import fields, Schema

from .model import DBTeam

class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    group = fields.String()

class Teams(object):
    schema = TeamSchema(many = True)

    def on_get(self, req, resp):
        req.context['result'] = self._session.query(DBTeam).all()

class Team(object):
    schema = TeamSchema()

    def on_get(self, req, resp, id):
        team = self._session.query(DBTeam).filter_by(id = id).one_or_none()
        if team:
            req.context['result'] = team
        else:
            resp.status = falcon.HTTP_NOT_FOUND
