import requests
import json

from freud.model import db
from freud.api.response import response_handler


def session_builder(req):
    s = requests.Session()
    request = requests.Request(req.method, req.url)

    headers = {
        'user-agent': 'Freud',
        'accept-encoding': 'gzip, deflate',
        'accept': '*/*',
        'connection': 'keep-alive',
        'charset': 'UTF-8',
    }
    request.headers = headers

    if req.auth:

        auth = json.loads(req.auth)
        authtype = auth.get('type')
        authuser = auth.get('user')
        authpass = auth.get('password')

        if authtype == 'basic':
            request.auth = (authuser, authpass)
        elif authtype == 'digest':
            request.auth = requests.auth.HTTPDigestAuth(
                authuser, authpass)

    if req.headers:
        headers = json.loads(req.headers)
        headers = {k.lower(): v.lower() for k, v in headers.items()}
        request.headers.update(headers)

    content_type = request.headers.get('content-type', None)

    if content_type:
        request.content_type = content_type

    request.data = req.body

    response = None
    errors = None

    try:
        response = s.send(request.prepare())

    except requests.exceptions.ConnectionError as e:
        errors = {'Connection error': str(e)}

    except requests.exceptions.RequestException as e:
        errors = {'Request Exception': str(e)}

    return [response, errors]


async def request_handler(name):

    # Get selected server url
    server = db.fetch_one(name=name)

    response, errors = session_builder(server)

    if errors:
        return {'errors': errors}

    headers, response_body = response_handler(response)

    return {'response': [headers, response_body]}
