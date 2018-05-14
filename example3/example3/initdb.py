import io

from .model import DBTeam

def init_db(session):
    init_teams(session)

def init_teams(session):
    with io.open('example3/data/teams.txt') as f:
        for line in f:
            fields = line.split('\t')
            session.add(DBTeam(name = fields[0]))
    session.commit()
