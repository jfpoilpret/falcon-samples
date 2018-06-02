import falcon
from marshmallow import fields, Schema
from ..utils.marshmallow_util import URLFor
from ..model import DBTeam

class TeamSchema(Schema):
	id = fields.Integer()
	href = URLFor('/team/{id}')
	name = fields.String(required=True)
	group = fields.String()
	played = fields.Integer()
	won = fields.Integer()
	drawn = fields.Integer()
	lost = fields.Integer()
	goals_for = fields.Integer()
	goals_against = fields.Integer()
	points = fields.Integer()

class Teams(object):
	schema = TeamSchema(many = True)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self._session.query(DBTeam).all()

class Team(object):
	schema = TeamSchema()

	def on_get(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		team = self._session.query(DBTeam).filter_by(id = id).one_or_none()
		if team:
			req.context['result'] = team
		else:
			resp.status = falcon.HTTP_NOT_FOUND
