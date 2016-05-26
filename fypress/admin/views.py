# -*- coding: UTF-8 -*-
from functools import wraps
from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from flask.ext.babel import lazy_gettext as gettext
from fypress.user import level_required, login_required, User, UserEditForm, UserAddForm
from fypress.item import FolderForm, Folder
import json

admin = Blueprint('admin', __name__,  url_prefix='/admin')

messages = {
    'updated'   : gettext('Item updated'),
    'added'     : gettext('Item added')
}

@admin.route('/')
@login_required
def root():
    return render_template('admin/index.html', title='Admin')


"""
    Posts
"""
@admin.route('/posts/new')
@level_required(1)
def posts_add():
    return render_template('admin/posts_new.html', title=gettext('New - Posts'))



"""
    Folders
"""
@admin.route('/folders', methods=['POST', 'GET'])
@admin.route('/folders/all', methods=['POST', 'GET'])
@level_required(3)
def folders():
    folders = Folder.get_all()
    folder  = None

    if request.args.get('edit') and request.args.get('edit') != 1:
        folder = Folder.query.get(request.args.get('edit'))
        form = FolderForm(obj=folder)
        if form.validate_on_submit():
            form.populate_obj(folder)
            folder.modified = 'NOW()'
            folder.update()
            flash(messages['updated']+' ('+str(folder)+')')
            return redirect(url_for('admin.folders'))
    else:
        form = FolderForm()
        if form.validate_on_submit():
            folder = Folder()
            form.populate_obj(folder)
            folder.created = 'NOW()'
            folder.parent  = 1
            Folder.query.add(folder)
            Folder.build_guid()
            flash(messages['added']+' ('+str(folder)+')')
            return redirect(url_for('admin.folders'))

    return render_template('admin/folders.html', folders=folders, folder=folder, title=gettext('Categories'), form=form)


"""
    Users
"""
@admin.route('/users')
@admin.route('/users/all')
@level_required(4)
def users():
    users = User.query.get_all()
    return render_template('admin/users.html', title=gettext('Users'), users=users)

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
        flash(messages['updated']+' ('+str(user)+')')
        return redirect(url_for('admin.users'))

    return render_template('admin/users_edit.html', title=gettext('Edit - Users'), user=user, form=form)

@admin.route('/users/new', methods=['POST', 'GET'])
@level_required(4)
def users_new():
    form = UserAddForm(request.form)

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        User.query.add(user)
        flash(messages['added']+' ('+str(user)+')')
        return redirect(url_for('admin.users'))

    return render_template('admin/users_new.html', title=gettext('New - Users'),  form=form)

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
                folder.update()
    return ''