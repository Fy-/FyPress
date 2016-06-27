# -*- coding: UTF-8 -*-
from flask_babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import TextField, validators, TextAreaField


class GeneralSettingsForm(Form):
    name = TextField(gettext(u'Site Title'), validators=[])
    slogan = TextField(gettext(u'Tagline'), description=gettext('In a few words, explain what this site is about.'), validators=[validators.required()])
    url = TextField(gettext(u'Site Address (URL)'), validators=[validators.required()])
    url = TextField(gettext(u'Site Address (URL)'), validators=[validators.required()])
    footer = TextAreaField(gettext(u'Footer text'))


class SocialSettingsForm(Form):
    analytics = TextField(gettext(u'Google Analytics'), description=gettext('Tacking ID: UA-XXXXXXXX-Y'), validators=[])
    facebook = TextField(gettext(u'Facebook Page'), validators=[])
    twitter = TextField(gettext(u'Twitter account'), validators=[])
    github = TextField(gettext(u'Github'), validators=[])
