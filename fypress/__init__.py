# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import SharedDataMiddleware
from flask import Flask, session, g
from flask.ext.babel import Babel
from config import config
from fypress.utils.mysql import FlaskFyMySQL
import time

class FyPress():
    def __init__(self, config):
        self.config = config
        self.app = Flask(
            __name__,
            template_folder=self.config.TEMPLATE_FOLDER,
            static_folder=self.config.STATIC_FOLDER
        )
        self.app.config.from_object(config)
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app)
        self.babel = Babel(self.app)
        self.db    = FlaskFyMySQL(self.app)

        self.prepare()

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port, debug=self.config.DEBUG)

    def prepare(self):
        @self.app.context_processor
        def inject_options():
            from fypress.utils.mysql.sql import FyMySQL

            return dict(options=g.options, queries=FyMySQL._instance.queries, debug=self.config.DEBUG, flask_config=self.app.config)

        @self.app.before_request
        def before_request():
            from fypress.user import User
            g.user = None
            if 'user_id' in session:
                g.user = User.query.get(session['user_id'])

            from fypress.admin import Option
            g.options = Option.auto_load()

        if self.config.DEBUG:
            @self.app.before_request
            def before_request():
                g.start = time.time()

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

fypress = FyPress(config)
