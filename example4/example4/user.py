import falcon
from sqlalchemy.orm.session import Session
from marshmallow import fields, Schema
from .marshmallow_util import URLFor, StrictSchema
from .falcon_util import update_item_fields
from .model import DBUser

#TODO improve read/write fields, hide some field depending on who is authenticated
class UserSchema(StrictSchema):
    id = fields.Integer()
    href = URLFor('/user/{id}')
    login = fields.String()
    password = fields.String()
    status = fields.String()
    admin = fields.Boolean()
    fullname = fields.String()
    email = fields.Email()
    creation = fields.DateTime()
    connection = fields.DateTime()

class Users(object):
    schema = UserSchema(many = True)

    def session(self):
        """:type: sqlalchemy.orm.Session"""
        # type: () -> Session
        return self._session

    def on_get(self, req, resp):
        # type: (falcon.Request, falcon.Response) -> None
        req.context['result'] = self.session().query(DBUser).all()
    
    def on_post(self, req, resp):
        # type: (falcon.Request, falcon.Response) -> None
        pass

#TODO User resource
class User(object):
    pass

