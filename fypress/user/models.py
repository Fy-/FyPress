# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, request
from flask.ext.babel import lazy_gettext as gettext
from fypress.utils import mysql
import urllib, hashlib

class UserMeta(mysql.Base):
    usermeta_id_user   = mysql.Column(etype='int', primary_key=True)
    usermeta_key       = mysql.Column(etype='string', primary_key=True)
    usermeta_value     = mysql.Column(etype='string')

class User(mysql.Base):
    user_id                 = mysql.Column(etype='int', primary_key=True)
    user_login              = mysql.Column(etype='string', unique=True)
    user_email              = mysql.Column(etype='string', unique=True)
    user_password           = mysql.Column(etype='string')
    user_nicename           = mysql.Column(etype='string')
    user_firstname          = mysql.Column(etype='string')
    user_lastname           = mysql.Column(etype='string')
    user_url                = mysql.Column(etype='string')
    user_registered         = mysql.Column(etype='datetime')
    user_activation_key     = mysql.Column(etype='string')
    user_status             = mysql.Column(etype='int')
    user_meta               = mysql.Column(obj=UserMeta, multiple='meta', link='usermeta_id_user')

    roles                   = {
        0: gettext('Member'),
        1: gettext('Contributor'),
        2: gettext('Author'),
        3: gettext('Editor'),
        4: gettext('Administrator')
    }

    roles_admin             = {
        0: gettext('<span class="badge alert-default">Member</span>'),
        1: gettext('<span class="badge alert-info">Contributor</span>'),
        2: gettext('<span class="badge alert-warning">Author</span>'),
        3: gettext('<span class="badge alert-danger">Editor</span>'),
        4: gettext('<span class="badge alert-success">Administrator</span>')   
    }

    def init(self):
        self.role = self.roles[self.status]
        self.role_admin = self.roles_admin[self.status]

    def has_level(self, level):
        if self.status >= level:
            return True
        return False

    def gravatar(self, size=50):
        default = "identicon"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

        return gravatar_url

    @property
    def password(self):
        if self.__dict__.has_key('password'):
            return self.__dict__['password']

    @password.setter
    def password(self, value):
        if 'pbkdf2:sha1:1000' in value:
            self.__dict__['password'] = value
        else:
            self.__dict__['password'] = generate_password_hash(value)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    @staticmethod
    def login(login, password):
        user = User.query.filter(login=login).one()
        if user.check_password(password):
            session['user_id'] = user.id
            user.meta['last_login'] = 'NOW()'
            user.meta['last_ip']    = request.remote_addr
            User.query.update(user)

            return True
        else:
            return False

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