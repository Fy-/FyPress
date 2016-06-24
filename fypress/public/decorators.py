from functools import wraps
from flask import request, g
from fypress import FyPress
import time

fypress = FyPress()

def cached(timeout=5*60, key='public-%s', pretty=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if fypress.config.CACHE == False or request.method == 'POST':
                if pretty == True:
                    return f(*args, **kwargs)
                return f(*args, **kwargs)

            cache_key = key % request.url
            rv = fypress.cache.get(cache_key)
            
            if rv is not None:
                try:
                    return rv+'\n\n<!-- FyPress Cache, served in {}s -->'.format(time.time() - g.start)
                except:
                    return rv

            if pretty == True:
                rv = f(*args, **kwargs)
            else:
                rv = f(*args, **kwargs)
            fypress.cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator