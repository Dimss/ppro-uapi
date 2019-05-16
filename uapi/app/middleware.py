import json
import falcon
import logging
from .exceptions import AppException


class JSONTranslator(object):
    def process_request(self, req, resp):
        body = req.stream.read()
        if body:
            try:
                req.context['doc'] = json.loads(body)
            except Exception as ex:
                logging.error(f"Unable to load body as JSON, ex: {str(ex)}")
                raise AppException(falcon.HTTP_406, "Not valid request body, only JSON supported")


class ResponseMiddleware(object):
    def process_response(self, req, resp, resource, req_succeeded):
        # Set body only if it's not already set by something else,
        # for example, by exception
        if resp.body is None:
            resp.status = resource.status
            resp.body = json.dumps({'status': 'ok', 'message': resource.message, 'data': resource.payload})
        # Cleanup resource status,message and data
        resource.status = falcon.HTTP_200
        resource.message = None
        resource.payload = None
