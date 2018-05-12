import io
import json
import falcon

from marshmallow import fields, Schema

class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

#FIXME issue with id sequence if we allow delete...
class Team(object):
    get_schema = TeamSchema(many = True)
    schema = TeamSchema()

    JSON_STORAGE = 'example2/data/teams.json'

    def __init__(self):
        # Read JSON storage
        with io.open(Team.JSON_STORAGE, 'r') as f:
            self._teams = json.load(f)

    def on_get(self, req, resp):
        req.context['result'] = self._teams

    def on_post(self, req, resp):
        new_team = req.context['json']
        new_team['id'] = len(self._teams) + 1
        self._teams.append(new_team)
        with io.open(Team.JSON_STORAGE, 'w') as f:
            json.dump(self._teams, f, indent = 4, ensure_ascii = False)
        req.context['result'] = new_team
        resp.status = falcon.HTTP_CREATED
