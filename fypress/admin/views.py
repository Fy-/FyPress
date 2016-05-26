# -*- coding: UTF-8 -*-
from functools import wraps
from flask import Blueprint, session, request, redirect, url_for, render_template
from fypress.user import level_required, login_required, User, UserEditForm, UserAddForm
from fypress.item import FolderForm, Folder
import json

admin = Blueprint('admin', __name__,  url_prefix='/admin')


@admin.route('/')
@login_required
def root():
    return render_template('admin/index.html', title='Admin')


"""
    Folders
"""
@admin.route('/folders', methods=['POST', 'GET'])
@admin.route('/folders/all', methods=['POST', 'GET'])
@level_required(3)
def folders():
    form = FolderForm()
    folders = Folder.get_all()

    

    if form.validate_on_submit():
        folder = Folder()
        form.populate_obj(folder)
        folder.created = 'NOW()'
        folder.parent  = 1
        Folder.query.add(folder)
        return redirect(url_for('admin.folders'))

    return render_template('admin/folders.html', folders=folders, title='Folders', form=form)


"""
    Users
"""
@admin.route('/users')
@admin.route('/users/all')
@level_required(4)
def users():
    users = User.query.get_all()
    return render_template('admin/users.html', title='Users', users=users)

@admin.route('/users/edit', methods=['POST', 'GET'])
@level_required(4)
def users_edit(id_user=None):
    if not id_user:
        id_user = request.args.get('id')

    user = User.query.get(id_user)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        User.query.update(user)
        return redirect(url_for('admin.users_edit', id=user.id))

    return render_template('admin/users_edit.html', title='Users', user=user, form=form)

@admin.route('/users/new', methods=['POST', 'GET'])
@level_required(4)
def users_new():
    form = UserAddForm(request.form)

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        User.query.add(user)
        return redirect(url_for('admin.users'))

    return render_template('admin/users_new.html', title='Users',  form=form)

@admin.route('/users/me', methods=['POST', 'GET'])
@login_required
def users_me():
    return users_edit(session.get('user_id'))


"""
    AJAX
"""
@admin.route('/folders/update', methods=['POST', 'GET'])
@level_required(3)
def ajax_folders():
    data = json.loads(request.form.get('data'))
    if data:
        for item in data:
            if item.has_key('id') and item['id'] != '1':
                folder = Folder.query.get(item['id'])
                folder.depth    = item['depth']
                folder.left     = item['left']
                folder.right    = item['right']
                folder.parent = item['parent_id']

                folder.modified = 'NOW()'
                Folder.query.update(folder)
    return ''