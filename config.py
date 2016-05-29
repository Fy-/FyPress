# -*- coding: UTF-8 -*-
import os

### BASE ###
BASE_DIR         = os.path.dirname(__file__)

### KEYS ###
CSRF_SESSION_KEY = "secretkeylol"

### CSRF ###
CSRF_ENABLED    = True
SECRET_KEY 		= "secretkeygglol"

### Babel ###
BABEL_DEFAULT_LOCALE    = 'en'
BABEL_DEFAULT_TIMEZONE  = 'UTC'

### MYSQL ###
MYSQL_USER 		= 'fypress'
MYSQL_PASSWORD	= 'stay'
MYSQL_DB		= 'fypress'
MYSQL_PREFIX	= 'fypress_'

### UPLOAD ###
MEDIA_ROOT           = os.path.join(BASE_DIR, 'media')
UPLOAD_DIRECTORY     = os.path.join(MEDIA_ROOT, 'uploads')
CHUNKS_DIRECTORY     = os.path.join(MEDIA_ROOT, 'chunks')
UPLOAD_DIRECTORY_URL = '/files/'

### DEBUG ###
DEBUG = True

del os

#template_folder=Config.THEME_FP['base'], 
#static_folder=Config.THEME_FP['base']+Config.THEME_FP['active']+'/static/',
#static_url_path='/static'