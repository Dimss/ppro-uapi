import json
import falcon
import logging
from .exceptions import AppException, BadToken
from .jwt import JWTValidator


class JSONTranslator(object):
    def process_request(self, req, resp):
        body = req.stream.read()
        if body:
            try:
                req.context['doc'] = json.loads(body)
            except Exception as ex:
                logging.error(f"Unable to load body as JSON, ex: {str(ex)}")
                raise AppException(falcon.HTTP_406, "Not valid request body, only JSON supported")


class AuthenticationMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        method = req.method
        resource_permissions = resource.resource_permissions()
        if method.lower() in resource_permissions['public']:
            logging.info("Accessing to public resource, not auth is required")
            return
        elif 'X-UAPI-AUTH' not in req.headers:
            logging.warning("Accessing to private resource, without auth token, request is forbidden")
            raise AppException(falcon.HTTP_401, "Unauthorized")
        else:
            token = req.headers['X-UAPI-AUTH']
            try:
                user = JWTValidator(token).validate_auth_data()
                req.context.user = user
            except BadToken:
                logging.warning("Not valid token")
                raise AppException(falcon.HTTP_401, "Unauthorized")


class CORSMiddleware(object):
    ALLOW_HEADERS = [
        'Access-Control-Allow-Headers',
        'Origin',
        'Accept',
        'X-Requested-With',
        'Content-Type',
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        'X-UAPI-AUTH'
    ]
    ALLOW_METHODS = [
        'GET',
        'POST',
        'OPTIONS',
        'PATCH',
        'PUT',
        'DELETE'
    ]

    def process_response(self, req, resp, resource, req_succeeded):
        if req.method == 'OPTIONS':
            cors_header = {
                'Access-Control-Allow-Origin': "%s" % req.env['HTTP_ORIGIN'],
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': ",".join(CORSMiddleware.ALLOW_METHODS),
                'Access-Control-Allow-Headers': ",".join(CORSMiddleware.ALLOW_HEADERS),
                'Content-Type': 'text/plain charset=UTF-8',
                'Content-Length': 0
            }
            resp.set_headers(cors_header)
            raise falcon.HTTPError(falcon.HTTP_OK)

        else:
            cors_header = {
                'Access-Control-Allow-Origin': "%s" % (req.env['HTTP_ORIGIN'] if 'HTTP_ORIGIN' in req.env else '*'),
                'Access-Control-Allow-Credentials': 'true',
            }
            resp.set_headers(cors_header)


class ResponseMiddleware(object):
    def process_response(self, req, resp, resource, req_succeeded):
        # Set body only if it's not already set by something else,
        # for example, by exception
        if resp.body is None:
            resp.status = resource.status
            resp.body = json.dumps({'status': 'ok', 'message': resource.message, 'data': resource.payload})
        # Cleanup resource status,message and data
        if resource:
            resource.status = falcon.HTTP_200
            resource.message = None
            resource.payload = None
