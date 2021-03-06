import ConfigParser
import os
from functools import wraps

from flask import request, Response

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.conf'))

server_username = config.get('SERVER', 'username')
server_password = config.get('SERVER', 'password')


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    print username
    return username == server_username and password == server_password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
