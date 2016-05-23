# -*- coding: UTF-8 -*-
from functools import wraps
from flask import Blueprint, session, request, redirect, url_for, render_template
from model import User
from form import UserLoginForm

user = Blueprint('user', __name__,  url_prefix='/user')

def login_required(f):
    @wraps(f)
    def login_is_required(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return login_is_required


@user.route('/')
@login_required
def root():
	return 'index'

@user.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user') and session['user']['id']:
        return redirect('/admin/')

    form = UserLoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        login = User.login(form.data['login'], form.data['password'])
        print login
        if login:
            if form.data['next'] != '':
                return redirect(form.data['next'])
            else:
                return redirect('/admin/')
    
    return render_template('admin/login.html', form=form, title="Please sign in")

@user.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@user.route('/blank')
def blank():
    return render_template('admin/blank.html', title='Admin')
