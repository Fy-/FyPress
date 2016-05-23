# -*- coding: UTF-8 -*-
import os

### BASE ###
_basedir = os.path.abspath(os.path.dirname(__file__))

### KEYS ###
CSRF_SESSION_KEY = "secretkeylol"

### CSRF ###
CSRF_ENABLED    = True
SECRET_KEY 		= "secretkeygglol"

### MYSQL ###
MYSQL_USER 		= 'fypress'
MYSQL_PASSWORD	= 'stay'
MYSQL_DB		= 'fypress'
MYSQL_PREFIX	= 'fypress_'

### DEBUG ###
DEBUG = True

del os

#template_folder=Config.THEME_FP['base'], 
#static_folder=Config.THEME_FP['base']+Config.THEME_FP['active']+'/static/',
#static_url_path='/static'