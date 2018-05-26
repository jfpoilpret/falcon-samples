import io
from datetime import datetime

from .model import DBTeam, DBVenue, DBMatch, DBUser

def init_db(session):
    init_teams(session)
    init_venues(session)
    init_matches(session)
    init_users(session)

def init_teams(session):
    with io.open('example4/data/teams.txt') as f:
        for line in f:
            fields = line[:-1].split('\t')
            session.add(DBTeam(name = fields[0], group = fields[1]))
    session.commit()

def init_venues(session):
    with io.open('example4/data/venues.txt') as f:
        for line in f:
            name = line[:-1]
            session.add(DBVenue(name = name))
    session.commit()

def init_users(session):
    with io.open('example4/data/users.txt') as f:
        for line in f:
            fields = line[:-1].split('\t')
            user = DBUser(  login = fields[0],
                            password = fields[1],
                            status = fields[2],
                            admin = fields[3].lower() in ('yes', 'true', '1'),
                            fullname = fields[4],
                            email = fields[5],
                            creation = datetime.strptime(fields[6], '%d/%m/%Y %H:%M'))
            session.add(user)
    session.commit()
    pass

#FIXME fix TZ (Moscow) to UTC, so that we use a common time reference!
def init_matches(session):
    with io.open('example4/data/matches.txt') as f:
        for line in f:
            fields = line[:-1].split('\t')
            venue = session.query(DBVenue).filter_by(name = fields[2]).one_or_none()
            team1 = session.query(DBTeam).filter_by(name = fields[3]).one_or_none()
            team2 = session.query(DBTeam).filter_by(name = fields[4]).one_or_none()
            match = DBMatch(round = fields[0],
                            matchtime = datetime.strptime(fields[1], '%d/%m/%Y %H:%M'),
                            venue = venue,
                            group = fields[5],
                            team1 = team1,
                            team2 = team2)
            session.add(match)
            session.commit()
