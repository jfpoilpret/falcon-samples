from datetime import datetime, timedelta, timezone

def to_naive_datetime(dt):
	# type: (datetime) -> datetime
	if dt and dt.tzinfo:
		return dt.astimezone(timezone.utc).replace(tzinfo = None)
	else:
		return dt

class TimeBase(object):
	def __init__(self):
		# type: () -> None
		self._delta = timedelta()

	def delta(self):
		# type () -> timedelta
		return self._delta

	def now(self):
		# type: () -> datetime
		return datetime.utcnow() + self._delta

	def reset(self):
		# type: () -> None
		self._delta = timedelta()
		
	def set_timebase(self, timebase):
		# type: (datetime) -> None
		self._delta = to_naive_datetime(timebase) - datetime.utcnow()

	def set_timedelta(self, delta):
		# type: (timedelta) -> None
		self._delta = self._delta + delta
