# -*- coding: UTF-8 -*-
from flask_babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import validators, TextField, TextAreaField, HiddenField
from wtforms.widgets import TextArea

class CommentForm(Form):
    content     = TextAreaField(gettext(u'Content'), widget=TextArea(), validators=[validators.required()])
    post_id     = HiddenField()
    parent      = HiddenField()

class GuestCommentForm(CommentForm):
    user_name       = TextField(gettext(u'Nickname'), validators=[validators.required()])
    user_email      = TextField(gettext(u'E-Mail'), validators=[validators.Email(), validators.required()])
    user_uri        = TextField(gettext(u'Website (URL)'), validators=[validators.required()])