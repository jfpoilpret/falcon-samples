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
    # Pattern to respect for result: XX-XX
    result = fields.String()

class Matches(object):
    schema = MatchSchema(many = True)

    def on_get(self, req, resp):
        # type: (falcon.Request, falcon.Response) -> None
        req.context['result'] = self._session.query(DBMatch).all()

# ADD PUT (or PATCH only?) to update a match (eg change time or venue or team or result)
class Match(object):
    schema = MatchSchema()
    patch_request_schema = MatchSchema(only = ('matchtime', 'venue.id', 'team1.id', 'team2.id', 'result'))

    def on_get(self, req, resp, id):
        # type: (falcon.Request, falcon.Response, int) -> None
        match = self._session.query(DBMatch).filter_by(id = id).one_or_none()
        if match:
            req.context['result'] = match
        else:
            resp.status = falcon.HTTP_NOT_FOUND

    def on_patch(self, req, resp, id):
        # type: (falcon.Request, falcon.Response, int) -> None
        match = self._session.query(DBMatch).filter_by(id = id).one_or_none()
        if match:
            values = req.context['json']
            update = False
            #TODO include it into _update() utility method
            for field in ('matchtime', 'venue.id', 'team1.id', 'team2.id', 'result'):
                update = Match._update(match, field, values) or update
            if update:
                self._session.add(match)
                self._session.commit()
                self._session.refresh(match)
            req.context['result'] = match
        else:
            resp.status = falcon.HTTP_NOT_FOUND

    #TODO Make this mehtod a general utility
    @staticmethod
    def _update(item, key, values):
        # type: (dict, str, dict) -> bool
        if key in values.keys():
            setattr(item, key, values[key])
            return True
        else:
            return False
