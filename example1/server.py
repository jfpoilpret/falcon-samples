from wsgiref.simple_server import make_server

from example1 import app
httpd = make_server('', 8000, app.api)
httpd.serve_forever()

