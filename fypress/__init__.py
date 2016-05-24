# -*- coding: UTF-8 -*-
from flask import Flask, session, g
from flask.ext.babel import Babel
import fy_mysql


app   = Flask(__name__)
app.config.from_object('config')

### Babel ###
babel = Babel(app)

### MySQL ###
db 	= fy_mysql.flask(app)

### Context ###
@app.context_processor
def inject_options():
    from fypress.admin import Option
    from fy_mysql.sql import FyMySQL
    return dict(options=Option.auto_load(), queries=FyMySQL._instance.queries, debug=app.config['DEBUG'])

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
