from functools import wraps
from flask import request, g, session
from fypress import FyPress
import time

fypress = FyPress()

def get_cache_key():
    return 'public-%s-%s' % (request.url, str(session.get('user_id')))

def cached(timeout=5*60, key='public-%s', pretty=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if fypress.config.CACHE == False or request.method == 'POST':
                return f(*args, **kwargs)

            cache_key = get_cache_key()
            rv = fypress.cache.get(get_cache_key())
            
            if rv is not None:
                try:
                    return rv+'\n\n<!-- FyPress Cache, served in {}s -->'.format(time.time() - g.start)
                except:
                    return rv

            rv = f(*args, **kwargs)
            fypress.cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator