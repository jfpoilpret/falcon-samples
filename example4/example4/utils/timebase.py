from datetime import datetime, timedelta

class TimeBase(object):
	def __init__(self):
		# type: () -> None
		self._delta = timedelta()

	def delta(self):
		# type () -> timedelta
		return self._delta

	def now(self):
		# type: () -> datetime
		return datetime.now() + self._delta

	def reset(self):
		# type: () -> None
		self._delta = timedelta()
		
	def set_timebase(self, timebase):
		# type: (datetime) -> None
		self._delta = timebase - datetime.now()

	def set_timedelta(self, delta):
		# type: (timedelta) -> None
		self._delta = self._delta + delta
