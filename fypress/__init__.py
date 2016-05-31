# -*- coding: UTF-8 -*-
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import SharedDataMiddleware

from flask import Flask, session, g
from flask.ext.babel import Babel
import fy_mysql

app   = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

### Statics ###
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

app.add_url_rule(app.config['UPLOAD_DIRECTORY_URL']+'<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {app.config['UPLOAD_DIRECTORY_URL']:  app.config['UPLOAD_DIRECTORY']})

### Babel ###
babel = Babel(app)

### MySQL ###
db 	= fy_mysql.flask(app)

### Context ###
@app.context_processor
def inject_options():
    from fypress.admin import Option
    from fy_mysql.sql import FyMySQL
    return dict(options=Option.auto_load(), queries=FyMySQL._instance.queries, debug=app.config['DEBUG'], flask_config=app.config)

@app.before_request
def before_request():
    from fypress.user import User
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

### Blueprints ###
from user import user_blueprint
from admin import admin_blueprint

### Load Blueprints ###
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint)

### Dev ###
