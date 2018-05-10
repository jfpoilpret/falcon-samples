import json
import falcon

class Team(object):
    def on_get(self, req,resp):
        teams = {
            'teams': [
                {
                    'name': 'France',
                    'href': '/team/1'
                }
            ]
        }
        resp.body = json.dumps(teams, ensure_ascii = False)


