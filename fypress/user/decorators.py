# -*- coding: UTF-8 -*-
from functools import wraps
from flask import g, session, redirect, url_for, request

def login_required(f):
    @wraps(f)
    def login_is_required(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return login_is_required

