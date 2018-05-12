import falcon
from falcon_marshmallow import Marshmallow
from wsgiref.simple_server import make_server

from .team import Team

api = application = falcon.API(middleware=[Marshmallow()])

api.add_route('/team', Team())
