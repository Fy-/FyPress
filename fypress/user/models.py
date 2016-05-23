# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import fy_mysql, urllib, hashlib

class User(fy_mysql.Base):
    # /sql/user.sql
    user_id                 = fy_mysql.Column(etype='int', primary_key=True)
    user_login              = fy_mysql.Column(etype='string', unique=True)
    user_email              = fy_mysql.Column(etype='string', unique=True)
    user_password           = fy_mysql.Column(etype='string')
    user_nicename           = fy_mysql.Column(etype='string')
    user_firstname          = fy_mysql.Column(etype='string')
    user_lastname           = fy_mysql.Column(etype='string')
    user_url                = fy_mysql.Column(etype='string')
    user_registered         = fy_mysql.Column(etype='datetime')
    user_activation_key     = fy_mysql.Column(etype='string')
    user_status             = fy_mysql.Column(etype='int')
    user_meta               = fy_mysql.Column(meta=True)

    def __init__(self):
        pass
    
    @property
    def password(self):
        if self.__dict__.has_key('password'):
            return self.__dict__['password']

    def gravatar(self, size=50):
        default = "http://www.example.com/default.jpg"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

        return gravatar_url

    @password.setter
    def password(self, value):
        if 'pbkdf2:sha1:1000' in value:
            self.__dict__['password'] = value
        else:
            self.__dict__['password'] = generate_password_hash(value)


    @staticmethod
    def login(login, password):
        user = User.query.filter(login=login).one()
        if user.check_password(password):
            session['user_id'] = user.id
            return True
        else:
            return False

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def add(login, email, password, data=None):
        if User.validate_email(email) and User.validate_login(login) and User.validate_password(password):
            user = User()

            user.login          = login
            user.email          = email
            user.password       = generate_password_hash(password)
            user.registered     = 'NOW()'
        
            User.query.add(user)

            return user         
        else:
            return False

    @staticmethod
    def validate_password(password):
        if 'pbkdf2:sha1:1000' not in password:
            return True
        else:
            return False

    @staticmethod
    def validate_login(login):
        return not User.query.exist('login', login)

    @staticmethod
    def validate_email( email):
        return not User.query.exist('email', email)

    def __repr__(self):
        return '[User: #%s %s (%s)]' % (self.id, self.nicename, self.email) 