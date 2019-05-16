import falcon
import logging
from uapi.app import bootstrap
from uapi.app.middleware import *
from uapi.app.exceptions import exception_serializer, generic_error_handler

# Init application
api = application = falcon.API(middleware=[JSONTranslator(), ResponseMiddleware()])
# Bootstrap application
bootstrap.init_routes(api)
# Register JSON exception serializer
api.set_error_serializer(exception_serializer)
# Register generic error handler
api.add_error_handler(Exception, generic_error_handler)
logging.info("Bootstrap is done, ready to process requests!")
