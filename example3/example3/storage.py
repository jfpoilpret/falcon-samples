import io
import json

#FIXME issue with id sequence when multi-threaded
class Storage(object):
    JSON_STORAGE = 'example3/data/teams.json'

    def __init__(self):
        # Read JSON storage
        with io.open(Storage.JSON_STORAGE, 'r') as f:
            self._teams = json.load(f)
        self._sequence = max(self._teams, key = lambda a:a['id'])['id']

    def _save(self):
        with io.open(Storage.JSON_STORAGE, 'w') as f:
            json.dump(self._teams, f, indent = 4, ensure_ascii = False)
        
    def teams(self):
        return self._teams
    
    def team(self, id):
        matches = filter(lambda a:a['id'] == id, self._teams)
        if matches:
            return matches[0]
        else:
            return None

    def add_team(self, team):
        self._sequence += 1
        team['id'] = self._sequence
        self._teams.append(team)
        self._save()
        return team

    def remove_team(self, id):
        for i, t in enumerate(self._teams):
            if t['id'] == id:
                del self._teams[i]
                self._save()
                return True
        return False
