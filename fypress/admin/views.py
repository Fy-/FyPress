# -*- coding: UTF-8 -*-
from functools import wraps
from flask import Blueprint, session, request, redirect, url_for, render_template
from fypress.user import login_required, User, UserEditForm

admin = Blueprint('admin', __name__,  url_prefix='/admin')


@admin.route('/')
@login_required
def root():
    return render_template('admin/index.html', title='Admin')

@admin.route('/users')
@login_required
def users():
    users = User.query.get_all()
    return render_template('admin/users.html', title='Users', users=users)

@admin.route('/users/edit')
@login_required
def users_edit():
    user = User.query.get(request.args.get('id'))
    form = UserEditForm(obj=user.std_object())
    print user.std_object()

    return render_template('admin/users_edit.html', title='Users', user=user, form=form)
