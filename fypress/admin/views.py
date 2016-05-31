# -*- coding: UTF-8 -*-
from flask import Blueprint, session, request, redirect, url_for, render_template, flash, jsonify, make_response
from flask.views import MethodView
from flask.ext.babel import lazy_gettext as gettext
from fypress.user import level_required, login_required, User, UserEditForm, UserAddForm
from fypress.folder import FolderForm, Folder
from fypress.media import Media
from fypress.post import Post
from fypress.admin.static import messages

import json

admin = Blueprint('admin', __name__,  url_prefix='/admin')

@admin.route('/')
@login_required
def root():
    return render_template('admin/index.html', title='Admin')

"""
    Posts
"""
@admin.route('/posts')
@admin.route('/posts/all')
@level_required(1)
def posts():
    posts = Post.query.filter(status='draft').all(array=True)+Post.query.filter(status='published').all(array=True)
    posts[0].dump()
    return render_template('admin/posts.html', title=gettext('Posts'), posts=posts)

@admin.route('/posts/new', methods=['POST', 'GET'])
@level_required(1)
def posts_add():
    post = Post()

    if request.args.get('edit'):
        post = Post.query.get(request.args.get('edit'))
        if post:
            if post.parent:
                return redirect(url_for('admin.posts_add', edit=post.parent))
            if request.form:
                post_id = Post.update(request.form, post)
                return redirect(url_for('admin.posts_add', edit=post_id))
        else:
            return '404'
    else:
        if request.form:
            post_id = Post.create(request.form)
            return redirect(url_for('admin.posts_add', edit=post_id))

    folders = Folder.get_all()
    return render_template('admin/posts_new.html', folders=folders, post=post, title=gettext('New - Post'))

"""
    Medias
"""
@admin.route('/medias')
@admin.route('/medias/all')
@level_required(1)
def medias():
    medias =  Media.query.get_all(array=True, order='ORDER BY `media_modified` DESC')

    return render_template('admin/medias.html',  medias=medias, title=gettext('Library - Medias'))

@admin.route('/medias/add/web')
@level_required(1)
def medias_web():
    return render_template('admin/medias_web.html',  title=gettext('Add from Web - Medias'))

@admin.route('/medias/add/upload')
@level_required(1)
def medias_upload():
    return render_template('admin/medias_upload.html',  title=gettext('Medias'))


"""
    Folders
"""
@admin.route('/folders', methods=['POST', 'GET'])
@admin.route('/folders/all', methods=['POST', 'GET'])
@level_required(3)
def folders():
    folders = Folder.get_all(True)
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
    users = User.query.get_all(array=True)
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

    return render_template('admin/users_edit.html', title=gettext('Edit - User'), user=user, form=form)

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

    return render_template('admin/users_new.html', title=gettext('New - User'),  form=form)

@admin.route('/users/me', methods=['POST', 'GET'])
@login_required
def users_me():
    return users_edit(session.get('user_id'))


"""
    POST
"""
@admin.route('/medias/upload', methods=['POST'])
@level_required(1)
def post_media():
    return Media.upload(request.files['qqfile'], request.form)


@admin.route('/medias/upload/<uuid>', methods=['POST'])
@level_required(1)
def post_media_delete():
    try:
        #handle_delete(uuid)
        return jsonify(success=True), 200
    except Exception, e:
        return jsonify(success=False, error=e.message), 400

"""
    AJAX
"""
@admin.route('/medias/get')
@level_required(1)
def ajax_get_media():
    media = Media.query.get(request.args.get('id').replace('media_', ''))
    result = {}
    result['name'] = media.name
    result['icon'] = media.icon
    result['guid'] = media.guid
    if media.type == 'image':
        result['var'] = media.data['var']
    if media.type == 'oembed':
        result['html'] = media.html
        
    return jsonify(data=result)

@admin.route('/medias/oembed/add', methods=['POST'])
@level_required(1)
def ajax_oembed_add():
    return Media.add_oembed(request.form)
    
@admin.route('/medias/oembed', methods=['POST'])
@level_required(1)
def ajax_oembed():
    data = request.form.get('data')
    return Media.add_from_web(data)

@admin.route('/folders/update', methods=['POST'])
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