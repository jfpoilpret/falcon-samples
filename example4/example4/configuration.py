import logging
import io
import os
from yaml import load
try:
	from yaml import CLoader as Loader
except:
	from yaml import Loader

class Configuration(object):
	def __init__(self):
		target = 'DEV'
		if 'CONFIG' in os.environ.keys():
			target = os.environ['CONFIG']
		with io.open('config.yaml', 'r') as f:
			all_config = load(f)
		if target not in all_config.keys():
			target = 'DEV'
		self._config = all_config[target]

	@property
	def db_type(self):
		return self._value('db_type')

	@property
	def db_name(self):
		return self._value('db_name')

	@property
	def drop_db(self):
		return self._value('drop_db', False)

	@property
	def log_output(self):
		return self._value('log_output', 'logs')

	@property
	def log_format(self):
		return self._value('log_format')

	@property
	def log_dateformat(self):
		return self._value('log_dateformat')

	@property
	def log_style(self):
		return self._value('log_style')

	@property
	def log_level(self):
		return self._get_level(self._value('log_level', 'INFO'))

	@property
	def timebase_changes(self):
		return self._value('timebase_changes', False)

	def _value(self, key, default = None):
		return self._config[key] if key in self._config else default
	
	def _get_level(self, level_name):
		levels = list(filter(lambda l: logging.getLevelName(l) == level_name, range(1, logging.CRITICAL)))
		if levels:
			return levels[0]
		else:
			return logging.INFO
