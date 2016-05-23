# -*- coding: UTF-8 -*-
from flask import Flask
import fy_mysql

app   = Flask(__name__)
app.config.from_object('config')

### MySQL ###
db 	= fy_mysql.flask(app)

### Context ###
from admin.model import Option
@app.context_processor
def inject_options():
    return dict(options=Option.auto_load())


### Blueprints ###
from user.controller import user 
from admin.controller import admin

### Load Blueprints ###
app.register_blueprint(user)
app.register_blueprint(admin)
