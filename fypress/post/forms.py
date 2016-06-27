# -*- coding: UTF-8 -*-
from flask_babel import lazy_gettext as gettext
from flask_wtf import Form
from wtforms import validators, TextField, TextAreaField, HiddenField
from wtforms.widgets import TextArea


class CommentForm(Form):
    content = TextAreaField(gettext(u'Content'), widget=TextArea(), validators=[validators.required()])


class GuestCommentForm(CommentForm):
    user_name = TextField(gettext(u'Nickname'), validators=[validators.required()])
    user_email = TextField(gettext(u'E-Mail'), validators=[validators.Email(), validators.required()])
    user_uri = TextField(gettext(u'Website (URL)'), validators=[validators.required()])


class LoggedCommentForm(CommentForm):
    pass


class AkismetForm(Form):
    api_key = TextField(gettext(u'Akismet API Key'), description=gettext(
        'If you want to prevent spam in your comments you need to configure your Akismet API key.'),  validators=[validators.required()])
