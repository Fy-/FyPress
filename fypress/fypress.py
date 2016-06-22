# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import SharedDataMiddleware
from flask import Flask, session, g
from flask_babel import Babel
from flask_fysql import FySQL
from .local import local
import time

class FyPress():
    def __init__(self, config, manager=False):
        self.prepared = False
        self.config = config
        self.app = Flask(
            __name__,
            template_folder=self.config.TEMPLATE_FOLDER,
            static_folder=self.config.STATIC_FOLDER
        )
        self.app.config.from_object(config)
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app)
        self.babel = Babel(self.app)
        self.database = FySQL(self.app)

        if not manager:
            self.prepare()

    def run(self, host='0.0.0.0', port=5000):
        if self.prepared == False:
            self.prepare()
        self.app.run(host=host, port=port, debug=self.config.DEBUG)

    def prepare(self):
        local.fp = self
        self.prepared = True

        @self.app.before_request
        def before_request():
            g.start = time.time()
            
        if self.config.DEBUG:
            @self.app.after_request
            def after_request(response):
                diff = time.time() - g.start
                if (response.response):
                    response.headers["Execution-Time"] = str(diff)
                return response

        self.app.add_url_rule(self.app.config['UPLOAD_DIRECTORY_URL']+'<filename>', 'FyPress.uploaded_file', build_only=True)
        self.app.wsgi_app = SharedDataMiddleware(self.app.wsgi_app, {self.app.config['UPLOAD_DIRECTORY_URL']: self.app.config['UPLOAD_DIRECTORY']})

        self.blueprint()

    def blueprint(self):
        ### Blueprints ###
        from user import user_blueprint
        from admin import admin_blueprint
        from public import public_blueprint

        ### Load Blueprints ###
        self.app.register_blueprint(user_blueprint)
        self.app.register_blueprint(admin_blueprint)
        self.app.register_blueprint(public_blueprint)

    @staticmethod
    def uploaded_file(filename):
        return send_from_directory(self.app.config['UPLOAD_DIRECTORY'], filename)
