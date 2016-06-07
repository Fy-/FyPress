# -*- coding: UTF-8 -*-
from flask import Blueprint, session, request, redirect, url_for, render_template, g

from fypress.user.models import User
from fypress.user.forms import UserLoginForm
from fypress.user.decorators import login_required

user = Blueprint('user', __name__,  url_prefix='/user')

@user.context_processor
def inject_options():
    from fypress.utils.mysql.sql import FyMySQL
    return dict(options=g.options, queries=FyMySQL._instance.queries)

@user.before_request
def before_request():
    from fypress.user import User
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

    from fypress.admin import Option
    g.options = Option.auto_load()

@user.route('/login', methods=['GET', 'POST'])
@user.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/admin/')

    form = UserLoginForm(request.form, next=request.args.get('next'))

    if form.validate_on_submit():
        login = User.login(form.data['login'], form.data['password'])
        if login:
            if form.data['next'] != '':
                return redirect(form.data['next'])
            else:
                return redirect('/admin/')
        else:
            pass
    
    return render_template('admin/login.html', form=form, title="Please sign in")

@user.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('user.login'))
