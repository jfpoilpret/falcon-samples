from wsgiref.simple_server import make_server

from example3 import app
httpd = make_server('', 8000, app.api)
httpd.serve_forever()
