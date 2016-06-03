# -*- coding: UTF-8 -*-
from functools import wraps, update_wrapper
from flask import g, session, redirect, url_for, request

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorator

def level_required(level):
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if session.get('user_id') is None:
                return redirect(url_for('user.login', next=request.url))

            if g.user.status < level:
                from fypress.admin import handle_403
                return handle_403()

            return f(*args, ** kwargs)
        return update_wrapper(wrapped_function, f)
    return decorator