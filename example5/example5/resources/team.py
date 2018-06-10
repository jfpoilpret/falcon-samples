import falcon
from marshmallow import fields, Schema
from ..utils import URLFor
from .resource import Resource
from ..model import DBTeam

class TeamSchema(Schema):
	id = fields.Integer()
	href = URLFor('/team/{id}')
	name = fields.String()
	group = fields.String()
	rank = fields.Integer()
	played = fields.Integer()
	won = fields.Integer()
	drawn = fields.Integer()
	lost = fields.Integer()
	goals_for = fields.Integer()
	goals_against = fields.Integer()
	goals_diff = fields.Integer()
	points = fields.Integer()

class Teams(Resource):
	schema = TeamSchema(many = True)

	def on_get(self, req, resp):
		# type: (falcon.Request, falcon.Response) -> None
		req.context['result'] = self.session().query(DBTeam).filter(DBTeam.group != 'virtual').all()

class Team(Resource):
	schema = TeamSchema()

	def on_get(self, req, resp, id):
		# type: (falcon.Request, falcon.Response, int) -> None
		self.check_and_set_result(req, 'team',
			self.session().query(DBTeam).filter(DBTeam.id == id, DBTeam.group != 'virtual').one_or_none())
