# -*- coding: utf-8 -*-
from werkzeug.contrib.cache import FileSystemCache, MemcachedCache, RedisCache
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import SharedDataMiddleware
from flask import Flask, session, g
from flask_babel import Babel
from flask_fysql import FySQL
from .utils import singleton

import time
import os

root = os.path.dirname(__file__)


@singleton
class FyPress(object):

    def __init__(self, config=False, manager=False):
        if config:
            self.cache = False
            self.prepared = False
            self.options = False

            self.config = config
            self.app = Flask(
                __name__,
                static_folder=os.path.join(root, '_html', 'static'),
                template_folder=config.THEME_FOLDER
            )
            self.app.config.from_object(config)
            self.app.wsgi_app = ProxyFix(self.app.wsgi_app)

            self.babel = Babel(self.app)
            self.database = FySQL(self.app)

            if not manager:
                self.prepare()

            self.blueprint()

    def run(self, host='0.0.0.0', port=5000):
        if self.prepared == False:
            self.prepare()

        self.app.run(host=host, port=port, debug=self.config.DEBUG)

    def prepare(self):
        self.prepared = True

        # Cache
        if self.config.CACHE_TYPE == 'redis':
            self.cache = RedisCache(host=self.config.CACHE_SERV)
        elif self.config.CACHE_TYPE == 'memcached':
            self.cache = MemcachedCache(servers=[self.config.CACHE_SERV])
        else:
            self.cache = FileSystemCache(self.config.CACHE_SERV)

        # Options
        from .admin import Option
        self.options = Option.auto_load()

        # Timer
        @self.app.before_request
        def before_request():
            g.start = time.time()

        # Medias
        self.app.add_url_rule(self.app.config['UPLOAD_DIRECTORY_URL'] + '<filename>', 'FyPress.uploaded_file', build_only=True)
        self.app.wsgi_app = SharedDataMiddleware(self.app.wsgi_app, {self.app.config['UPLOAD_DIRECTORY_URL']: self.app.config['UPLOAD_DIRECTORY']})

    def blueprint(self):
        ### Blueprints ###
        from admin import admin_blueprint
        from public import public_blueprint

        ### Load Blueprints ###
        self.app.register_blueprint(admin_blueprint)
        self.app.register_blueprint(public_blueprint)

    @staticmethod
    def uploaded_file(filename):
        return send_from_directory(self.app.config['UPLOAD_DIRECTORY'], filename)
