from functools import wraps
from flask_login import current_user
from flask import abort

def requires_roles(*roles):
    def deco(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Simple placeholder: extend to real roles linked to user
            if not current_user.is_authenticated:
                abort(401)
            # For the scaffold, allow all authenticated; customize later
            return f(*args, **kwargs)
        return wrapper
    return deco
