# -*- coding: UTF-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField, validators

class UserLoginForm(Form):
    login       = TextField(u'Login', validators=[validators.required()])
    password    = PasswordField(u'Password', validators=[validators.required()])
    remember_me = BooleanField(u'Remember Me')
    next        = HiddenField()

class UserEditForm(Form):
    login       = TextField(u'Login', validators=[validators.required()])
    #password    = PasswordField(u'Password', validators=[validators.required()])
    email       = TextField(u'E-Mail', validators=[validators.Email(), validators.required()])
    nicename    = TextField(u'Nicename', validators=[validators.required()])
    firstname   = TextField(u'Firstname', validators=[validators.required()])
    lastname    = TextField(u'Lastname', validators=[validators.required()])
    url         = TextField(u'URL', validators=[validators.required()])