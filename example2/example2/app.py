import falcon

from .team import Team

api = application = falcon.API()
api.add_route('/team', Team())

