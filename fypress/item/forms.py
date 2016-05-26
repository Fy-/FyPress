# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import validators, TextField, TextAreaField
from wtforms.widgets import TextArea
from fypress.user.models import User

class FolderForm(Form):
    name        = TextField(gettext(u'Name'), validators=[validators.required()])
    slug        = TextField(gettext(u'Slug'), validators=[validators.required()])
    content     = TextAreaField(gettext(u'Content'), widget=TextArea(), validators=[validators.required()])
    seo_content = TextAreaField(gettext(u'SEO Content'), widget=TextArea(), validators=[validators.required()])
