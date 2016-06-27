# -*- coding: utf-8 -*-
from fysql.databases import MySQLDatabase

from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class FySQL(object):
    engines = {
        'MySQL': MySQLDatabase
    }

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        engine = self.app.config['DATABASE']['engine']
        self.db_name = self.app.config['DATABASE']['db']

        self.conn_kwargs = {}
        for key, attr in self.app.config['DATABASE'].items():
            if key not in ['engine', 'db']:
                self.conn_kwargs[key] = attr

        self.engine = self.engines[engine]

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        self.db = self.init_db()

    def init_db(self):
        return self.engine(self.db_name, **self.conn_kwargs)

    def teardown(self, exception):
        self.db.close()
