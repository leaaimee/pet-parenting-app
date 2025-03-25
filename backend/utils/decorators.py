from functools import wraps
from flask import abort
from flask_login import current_user

def requires_permission(permission):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if permission not in current_user.permissions:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator