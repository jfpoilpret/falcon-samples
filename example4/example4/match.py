import re
import falcon
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema, validates, ValidationError
from .marshmallow_util import URLFor, StrictSchema
from .falcon_util import update_item_fields
from .model import DBMatch

class MatchSchema(Schema):
    id = fields.Integer()
    href = URLFor('/match/{id}')
    round = fields.String()
    matchtime = fields.DateTime()
    venue = fields.Nested('VenueSchema')
    team1 = fields.Nested('TeamSchema')
    team2 = fields.Nested('TeamSchema')
    group = fields.String()
    result = fields.String()

class MatchPatchSchema(StrictSchema):
    matchtime = fields.DateTime()
    venue_id = fields.Integer()
    team1_id = fields.Integer()
    team2_id = fields.Integer()
    result = fields.String(allow_none=True)

    RESULT_PATTERN = re.compile(r'[1-9]?[0-9]-[1-9]?[0-9]')

    @validates('result')
    def verify_result(self, value):
        if value and not MatchPatchSchema.RESULT_PATTERN.match(value):
            raise ValidationError('result must comply to format "0-0"', 'result')

class Matches(object):
    schema = MatchSchema(many = True)

    def on_get(self, req, resp):
        # type: (falcon.Request, falcon.Response) -> None
        req.context['result'] = self._session.query(DBMatch).all()

class Match(object):
    schema = MatchSchema()
    patch_request_schema = MatchPatchSchema()

    #TODO attempt to have code completion on SQLAlchemy session: generalize it?
    def session(self):
        # type: () -> Session
        return self._session

    def on_get(self, req, resp, id):
        # type: (falcon.Request, falcon.Response, int) -> None
        match = self.session().query(DBMatch).filter_by(id = id).one_or_none()
        if match:
            req.context['result'] = match
        else:
            resp.status = falcon.HTTP_NOT_FOUND

    def on_patch(self, req, resp, id):
        # type: (falcon.Request, falcon.Response, int) -> None
        session = self.session()
        match = session.query(DBMatch).filter_by(id = id).one_or_none()
        if match:
            values = req.context['json']
            if update_item_fields(match, Match.patch_request_schema.fields, values):
                session.add(match)
                session.commit()
                session.refresh(match)
            req.context['result'] = match
        else:
            resp.status = falcon.HTTP_NOT_FOUND

