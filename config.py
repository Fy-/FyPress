# -*- coding: UTF-8 -*-
import os

class Config(object):
    ### BASE ###
    BASE_DIR         = os.path.dirname(__file__)

    ### KEYS ###
    CSRF_SESSION_KEY = "secretkeylol"

    ### CSRF ###
    CSRF_ENABLED    = True
    SECRET_KEY 		= "secretkeygglol"

    ### Folders ###
    STATIC_FOLDER     = os.path.join(BASE_DIR, 'static')
    TEMPLATE_FOLDER   = os.path.join(BASE_DIR, 'templates')

    ### Babel ###
    BABEL_DEFAULT_LOCALE    = 'en'
    BABEL_DEFAULT_TIMEZONE  = 'UTC'

    ### MYSQL ###
    MYSQL_USER 		= 'dev'
    MYSQL_PASSWORD	= 'pwd'
    MYSQL_DB		= 'dev'
    MYSQL_PREFIX	= 'fypress_'

    ### UPLOAD ###
    MEDIA_ROOT           = os.path.join(BASE_DIR, 'media')
    UPLOAD_DIRECTORY     = os.path.join(MEDIA_ROOT, 'uploads')
    CHUNKS_DIRECTORY     = os.path.join(MEDIA_ROOT, 'chunks')
    UPLOAD_DIRECTORY_URL = '/files/'

    ### DEBUG ###
    DEBUG = True
    CACHE = True

    ### CACHE ###
    CACHE_TYPE = 'memcached' # redis, memcached, file
    CACHE_SERV = '127.0.0.1' # 127.0.0.1, 127.0.0.1, cache/ 

    ### URL ###
    URL        = 'http://127.0.0.1:5000/'

class ConfigProd(Config):
    DEBUG = True
    CACHE = True


del os
