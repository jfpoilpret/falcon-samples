import io
from datetime import datetime, timezone
import logging
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func

from .model import DBTeam, DBVenue, DBMatch, DBUser
from .utils.auth import hash_password

logger = logging.getLogger(__name__)

def init_db(session, tz):
	# type: (Session, str) -> None
	# Check if DB is empty
	if not session.query(func.count('*')).select_from(DBTeam).scalar():
		init_teams(session)
	if not session.query(func.count('*')).select_from(DBVenue).scalar():
		init_venues(session)
	if not session.query(func.count('*')).select_from(DBMatch).scalar():
		init_matches(session, tz)
	if not session.query(func.count('*')).select_from(DBUser).scalar():
		init_users(session)

def init_teams(session):
	# type: (Session) -> None
	with io.open('example4/data/teams.txt') as f:
		for line in f:
			fields = line[:-1].split('\t')
			session.add(DBTeam(name = fields[0], group = fields[1]))
	session.commit()

def init_venues(session):
	# type: (Session) -> None
	with io.open('example4/data/venues.txt') as f:
		for line in f:
			name = line[:-1]
			session.add(DBVenue(name = name))
	session.commit()

def init_users(session):
	# type: (Session) -> None
	with io.open('example4/data/users.txt') as f:
		for line in f:
			fields = line[:-1].split('\t')
			user = DBUser(  email = fields[0],
							password = hash_password(fields[1]),
							status = fields[2],
							admin = fields[3].lower() in ('yes', 'true', '1'),
							fullname = fields[4],
							creation = datetime.strptime(fields[5], '%d/%m/%Y %H:%M'))
			session.add(user)
	session.commit()

def init_matches(session, tz):
	# type: (Session, str) -> None
	with io.open('example4/data/matches.txt') as f:
		num = 1
		for line in f:
			fields = line[:-1].split('\t')
			venue = session.query(DBVenue).filter_by(name = fields[2]).one_or_none()
			team1 = session.query(DBTeam).filter_by(name = fields[3]).one_or_none()
			team2 = session.query(DBTeam).filter_by(name = fields[4]).one_or_none()
			matchtime = datetime.strptime(fields[1] + ' ' + tz, '%d/%m/%Y %H:%M %z').astimezone(timezone.utc).replace(tzinfo = None)
			match = DBMatch(matchnumber = num,
							round = fields[0],
							matchtime = matchtime,
							venue = venue,
							group = fields[5],
							team1 = team1,
							team2 = team2)
			logger.debug('matchtime %s (%s)' % (match.matchtime, match.matchtime.isoformat()))
			session.add(match)
			session.commit()
			logger.debug('Adding match %s' % str(match))
			num = num + 1
