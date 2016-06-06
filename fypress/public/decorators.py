from werkzeug.contrib.cache import FileSystemCache, MemcachedCache, RedisCache
from flask import g
from functools import wraps
from flask import request
from config import config
from bs4 import BeautifulSoup 
from config import config
import time

if config.CACHE_TYPE == 'redis':
    cache = RedisCache(host=config.CACHE_SERV)
elif config.CACHE_TYPE == 'memcached':
    cache = MemcachedCache(servers=[config.CACHE_SERV])
else:
    cache = FileSystemCache(config.CACHE_SERV)

def clean_html(buf):
    bs = BeautifulSoup(buf, 'html5lib')
    return bs.prettify(formatter="minimal")

def cached(timeout=5*60, key='public%s', pretty=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if config.CACHE == False:
                if pretty == True:
                    return clean_html(f(*args, **kwargs))
                return f(*args, **kwargs)

            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv+'\n\n<!-- FyPress Cache, served in {}s -->'.format(time.time() - g.start)

            if pretty == True:
                rv = clean_html(f(*args, **kwargs))
            else:
                rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator