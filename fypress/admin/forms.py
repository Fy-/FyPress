# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import TextField, validators

class GeneralSettingsForm(Form):
    name     = TextField(gettext(u'Site Title'), validators=[validators.required()])
    slogan   = TextField(gettext(u'Tagline'), description=gettext('In a few words, explain what this site is about.'), validators=[validators.required()])
    url      = TextField(gettext(u'Site Address (URL)'), validators=[validators.required()])

