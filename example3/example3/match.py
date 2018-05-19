import falcon
from marshmallow import fields, Schema
from .marshmallow_util import URLFor
from .model import DBMatch
from .team import TeamSchema
from .venue import VenueSchema

class MatchSchema(Schema):
    id = fields.Integer()
    href = URLFor('/match/{id}')
    round = fields.String()
    matchtime = fields.DateTime()
    venue = fields.Nested(VenueSchema)
    team1 = fields.Nested(TeamSchema)
    team2 = fields.Nested(TeamSchema)
    group = fields.String()
    result = fields.String()

class Matches(object):
    schema = MatchSchema(many = True)

    def on_get(self, req, resp):
        req.context['result'] = self._session.query(DBMatch).all()

# ADD PUT (or PATCH only?) to update a match (eg change time or venue or team or result)
class Match(object):
    schema = MatchSchema()

    def on_get(self, req, resp, id):
        Match = self._session.query(DBMatch).filter_by(id = id).one_or_none()
        if Match:
            req.context['result'] = Match
        else:
            resp.status = falcon.HTTP_NOT_FOUND
