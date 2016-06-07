# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import TextField, validators

class GeneralSettingsForm(Form):
    name     = TextField(gettext(u'Site Title'), validators=[])
    slogan   = TextField(gettext(u'Tagline'), description=gettext('In a few words, explain what this site is about.'), validators=[validators.required()])
    url      = TextField(gettext(u'Site Address (URL)'), validators=[validators.required()])

class SocialSettingsForm(Form):
    facebook = TextField(gettext(u'Facebook Page'), description=gettext('In a few words, explain what this site is about.'), validators=[])
    twitter  = TextField(gettext(u'Twitter account'), description=gettext('In a few words, explain what this site is about.'), validators=[])
    github   = TextField(gettext(u'Github repository'), description=gettext('In a few words, explain what this site is about.'), validators=[])

