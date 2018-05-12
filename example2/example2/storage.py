import io
import json

#FIXME issue with id sequence when multi-threaded
class Storage(object):
    JSON_STORAGE = 'example2/data/teams.json'

    def __init__(self):
        # Read JSON storage
        with io.open(Storage.JSON_STORAGE, 'r') as f:
            self._teams = json.load(f)
        self._sequence = max(self._teams, key = lambda a:a['id'])['id']

    def teams(self):
        return self._teams

    def add_team(self, team):
        self._sequence += 1
        team['id'] = self._sequence
        self._teams.append(team)
        with io.open(Storage.JSON_STORAGE, 'w') as f:
            json.dump(self._teams, f, indent = 4, ensure_ascii = False)
        return team
