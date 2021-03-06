import falcon
import threading
from marshmallow import Schema, fields, validates_schema, ValidationError

class ContextMiddleware(object):
    def __init__(self):
        self._context = threading.local()

    def context(self):
        return self._context

    def process_request(self, req, resp):
        # type: (falcon.Request, falcon.Response) -> None
        print('uri = %s' % req.uri)
        print('prefix = %s' % req.prefix)
        self._context.uri = req.uri
        self._context.prefix = req.prefix

# Create context middleware
context_middleware = ContextMiddleware()

class URLFor(fields.FormattedString):
    def __init__(self, uri_template, *args, **kwargs):
        # type: (str, list, dict) -> None
        self._context = context_middleware.context()
        fields.FormattedString.__init__(self, uri_template, *args, **kwargs)

    def _serialize(self, value, key, obj):
        # type: (object, str, object) -> None
        return self._context.prefix + fields.FormattedString._serialize(self, value, key, obj)

class StrictSchema(Schema):
    @validates_schema(pass_original=True)
    def reject_extra_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)

