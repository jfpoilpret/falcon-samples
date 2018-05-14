import falcon
from marshmallow import fields, Schema

from .model import DBTeam

#TODO review acceptable methods (no reason to create or delete team, even changing team is probably useless)
class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    group = fields.String()

class Teams(object):
    get_schema = TeamSchema(many = True)
    schema = TeamSchema()

    def on_get(self, req, resp):
        req.context['result'] = self._session.query(DBTeam).all()

    def on_post(self, req, resp):
        #TODO exception handling? (primary key, other constraints...)
        team = DBTeam(**req.context['json'])
        self._session.add(team)
        self._session.commit()
        self._session.refresh(team)
        req.context['result'] = team
        resp.status = falcon.HTTP_CREATED

class Team(object):
    schema = TeamSchema()

    def on_get(self, req, resp, id):
        team = self._session.query(DBTeam, id = id).one_or_none()
        if team:
            req.context['result'] = team
        else:
            resp.status = falcon.HTTP_NOT_FOUND

    def on_delete(self, req, resp, id):
        team = self._session.query(DBTeam, id = id).one_or_none()
        if not team:
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            self._session.delete(team)
            resp.status = falcon.HTTP_NO_CONTENT

    #TODO put, patch
