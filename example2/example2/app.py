import falcon
from falcon_marshmallow import Marshmallow
from wsgiref.simple_server import make_server

from .storage import Storage
from .team import Team, Teams

api = application = falcon.API(middleware=[Marshmallow()])

storage = Storage()
api.add_route('/team', Teams(storage))
api.add_route('/team/{id:int}', Team(storage))
