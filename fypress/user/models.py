# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, request
from flask_babel import lazy_gettext as gettext
from fypress.models import FyPressTables
from fysql import CharColumn, DateTimeColumn, IntegerColumn, DictColumn
import urllib, hashlib, datetime

def password_setter(value):
    if 'pbkdf2:sha1:1000' in value:
        return value
    return generate_password_hash(value)

class User(FyPressTables):
    login            = CharColumn(unique=True, index=True, max_length=75)
    email            = CharColumn(unique=True, index=True, max_length=150)
    password         = CharColumn(max_length=100, setter=password_setter)
    nicename         = CharColumn(max_length=200)
    firstname        = CharColumn(max_length=75)
    lastname         = CharColumn(max_length=75)
    url              = CharColumn(max_length=200)
    registered       = DateTimeColumn(default=datetime.datetime.now)
    activation_key   = CharColumn(max_length=200)
    status           = IntegerColumn()
    meta             = DictColumn()

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

    def __load__(self):
        self.role = self.roles[self.status]
        self.role_admin = self.roles_admin[self.status]

    def has_level(self, level):
        if self.status >= level:
            return True
        return False

    def gravatar(self, size=50):
        default = "identicon"
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

        return gravatar_url    

    def check_password(self, password):
        a = generate_password_hash(password)
        return check_password_hash(self.password, password)

    @staticmethod
    def connect(login, password):
        user = User.filter(User.login==login).one()
        if user.check_password(password):
            session['user_id'] = user.id
            user.meta['last_login'] = datetime.datetime.now()
            user.meta['last_ip']    = request.remote_addr
            user.save()

            return True
        else:
            return False

    @staticmethod
    def add(login, email, password, data=None):
        if User.validate_email(email) and User.validate_login(login) and User.validate_password(password):
            return User.create(
                login=login, 
                email=email, 
                password=generate_password_hash(password)
            )
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
        return not User.filter(User.login==login).one()

    @staticmethod
    def validate_email( email):
        return not User.filter(User.email==email).one()