from functools import wraps
from flask import request
from bs4 import BeautifulSoup 
from fypress.local import _fypress_
import time

config  = _fypress_.config
cache   = _fypress_.cache

def clean_html(buf):
    if isinstance(buf, tuple):
        bs = BeautifulSoup(buf[0], 'html5lib')
        return (bs.prettify(formatter="minimal"), buf[1])
    else:
        bs = BeautifulSoup(buf, 'html5lib')
        return bs.prettify(formatter="minimal")

def cached(timeout=5*60, key='public-%s', pretty=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if config.CACHE == False:
                if pretty == True:
                    return clean_html(f(*args, **kwargs))
                return f(*args, **kwargs)

            cache_key = key % request.url
            rv = cache.get(cache_key)
            if rv is not None:
                try:
                    return rv+'\n\n<!-- FyPress Cache, served in {}s -->'.format(time.time() - g.start)
                except:
                    return rv

            if pretty == True:
                rv = clean_html(f(*args, **kwargs))
            else:
                rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator