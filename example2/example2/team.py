import io
import json
import falcon

#FIXME issue with id sequence if we allow delete...
class Team(object):
    JSON_STORAGE = 'example2/data/teams.json'

    def __init__(self):
        # Read JSON storage
        with io.open(Team.JSON_STORAGE, 'r') as f:
            self._teams = json.load(f)

    def on_get(self, req, resp):
        resp.body = json.dumps(self._teams, ensure_ascii = False)

    def on_post(self, req, resp):
        new_team = json.load(req.stream)
        new_team['id'] = len(self._teams) + 1
        self._teams.append(new_team)
        with io.open(Team.JSON_STORAGE, 'w') as f:
            json.dump(self._teams, f, indent = 4, ensure_ascii = False)
        resp.body = json.dumps(new_team, ensure_ascii = False)
        resp.status = falcon.HTTP_CREATED
