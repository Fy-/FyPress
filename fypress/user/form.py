from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField, validators

class UserLoginForm(Form):
	login 		= TextField(u'Login', validators=[validators.required()])
	password 	= PasswordField(u'Password', validators=[validators.required()])
	remember_me = BooleanField(u'Remember Me')
	next		= HiddenField()
