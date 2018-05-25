import logging
from falcon import HTTPError

logger = logging.getLogger(__name__)

def update_item_fields(item, keys, values):
    # type: (dict, list, dict) -> bool
    update = False
    for key in keys:
        if key in values.keys():
            setattr(item, key, values[key])
            update = True
    return update

class ExceptionHandler(object):
    def __init__(self, status, title):
        # type: (str, str) -> None
        self._status = status
        self._title = title

    def __call__(self, ex, req, resp, params):
        # type: (Exception, falcon.Request, falcon.response, dict) -> None
		logger.warning('Exception occurred on request %s %s', req.method, req.uri, exc_info = ex)
        raise HTTPError(self._status, self._title, str(ex))

