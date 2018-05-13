from sqlalchemy.orm import scoped_session, sessionmaker

class SqlAlchemy(object):
    def __init__(self, engine):
        factory = sessionmaker(bind = engine)
        self._session_holder = scoped_session(factory)
    
    def new_session(self):
        return self._session_holder()

    def delete_session(self):
        self._session_holder.remove()

    def process_resource(self, req, resp, resource, params):
        resource._session = self.new_session()

    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            resource._session.commit()
        self.delete_session()
