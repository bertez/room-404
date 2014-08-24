from functools import wraps
from flask import request, Response

username_404 = 'guest'
pass_404 = 'CHANGE-ME'

try:
    from production_cfg import pass_404
except ImportError:
    pass

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == username_404 and password == pass_404

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Admin Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
