# -*- coding: UTF-8 -*-
from flask_babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField, validators, SelectField
from fypress.user.models import User

class UserLoginForm(Form):
    login       = TextField(gettext(u'Login'), validators=[validators.required()])
    password    = PasswordField(gettext(u'Password'), validators=[validators.required()])
    #remember_me = BooleanField(gettext(u'Remember Me'))
    next        = HiddenField()

class UserEditForm(Form):
    login       = TextField(gettext(u'Login'), validators=[validators.required()])
    email       = TextField(gettext(u'E-Mail'), validators=[validators.Email(), validators.required()])
    nicename    = TextField(gettext(u'Nicename'), validators=[validators.required()])
    firstname   = TextField(gettext(u'Firstname'), validators=[])
    lastname    = TextField(gettext(u'Lastname'), validators=[])
    url         = TextField(gettext(u'URL'), validators=[])

class UserEditFormAdmin(UserEditForm):
    status      = SelectField(gettext(u'Role'), choices=[('0', gettext('Member')), ('1', gettext('Contributor')), ('2', gettext('Author')), ('3', gettext('Editor')), ('4', gettext('Administrator'))])


class UserAddForm(Form):
    login       = TextField(gettext(u'Login'), validators=[validators.required()])

    password    = PasswordField(gettext(u'Password'), validators=[validators.required()])
    password_c  = PasswordField(gettext(u'Repeat Password'), validators=[
        validators.required(),
        validators.EqualTo('password', message=gettext('Passwords must match'))
    ])
    status      = SelectField(gettext(u'Role'), choices=[('0', gettext('Member')), ('1', gettext('Contributor')), ('2', gettext('Author')), ('3', gettext('Editor')), ('4', gettext('Administrator'))])

    email       = TextField(gettext(u'E-Mail'), validators=[validators.Email(), validators.required()])
    nicename    = TextField(gettext(u'Nicename'), validators=[validators.required()])
    firstname   = TextField(gettext(u'Firstname'), validators=[])
    lastname    = TextField(gettext(u'Lastname'), validators=[])
    url         = TextField(gettext(u'URL'), validators=[])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not User.validate_login(self.login.data):
            self.login.errors.append(gettext('Login already taken'))
            return False

        if not User.validate_email(self.email.data):
            self.email.errors.append(gettext('E-Mail already taken'))
            return False

        return True


