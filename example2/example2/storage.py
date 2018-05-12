import io
import json

class Storage(object):
    JSON_STORAGE = 'example2/data/teams.json'

    def __init__(self):
        # Read JSON storage
        with io.open(Storage.JSON_STORAGE, 'r') as f:
            self._teams = json.load(f)

    def teams(self):
        return self._teams

    def add_team(self, team):
        team['id'] = len(self._teams) + 1
        self._teams.append(team)
        with io.open(Storage.JSON_STORAGE, 'w') as f:
            json.dump(self._teams, f, indent = 4, ensure_ascii = False)
        return team
