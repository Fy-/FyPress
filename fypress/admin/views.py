# -*- coding: UTF-8 -*-
from flask import Blueprint, session, request, redirect, url_for, flash, jsonify, make_response, g, get_flashed_messages
from flask.templating import _default_template_ctx_processor
from jinja2 import Environment, PackageLoader
from flask_babel import lazy_gettext as gettext
from fypress.user import level_required, login_required, User, UserEditForm, UserAddForm, UserEditFormAdmin, UserLoginForm
from fypress.folder import FolderForm, Folder
from fypress.media import Media
from fypress.post import Post, SimpleComment, AkismetForm
from fypress.admin.static import messages
from fypress.admin.forms import GeneralSettingsForm, SocialSettingsForm
from fypress.admin.models import Option, Theme
from fypress.utils import get_redirect_target, Paginator
from fypress import __version__, __file__ as __fypress_file__, FyPress

import json, datetime

admin  = Blueprint('admin', __name__,  url_prefix='/admin')
fypress = FyPress()

env    = Environment(loader=PackageLoader('fypress', '_html/templates/'),  extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_'], autoescape=True)

def render_template(template, **kwargs):
    kwargs.update(_default_template_ctx_processor())
    kwargs.update({
        'url_for': url_for,
        'get_flashed_messages': get_flashed_messages,
        '_': gettext
    })
    kwargs.update(dict(options=g.options, version=__version__, debug=fypress.config.DEBUG, flask_config=fypress.config))

    template = env.get_template(template)
    return template.render(**kwargs)

@admin.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.get(User.id==session['user_id'])

    g.options = Option.auto_load()

@admin.after_request
def clear_cache(response):
    # todo, button clear cache
    if fypress.cache:
        fypress.cache.clear()
    return response

@admin.route('/')
@login_required
def root():
    return render_template('admin/index.html', title='Admin')

"""
    Login & Logout
"""
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/admin/')

    form = UserLoginForm(request.form, next=request.args.get('next'))

    if form.validate_on_submit():
        login = User.connect(form.data['login'], form.data['password'])
        if login:
            if form.data['next'] != '':
                return redirect(form.data['next'])
            else:
                return redirect('/admin/')
        else:
            pass
    
    return render_template('admin/login.html', form=form, title=gettext('Please sign in'))

@admin.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


"""
    Errors & Utils
"""
@admin.route('/back')
def back():
    return redirect(get_redirect_target())

def handle_404():
    return render_template('admin/404.html', title=gettext('Error: 404')), 404

def handle_403():
    return render_template('admin/403.html', title=gettext('Error: 403')), 403



"""
    Themes
"""
@admin.route('/themes')
@level_required(4)
def themes():
    themes = Theme.load_themes()
    
    return render_template('admin/themes.html', themes=themes, title=gettext('Theme'))

@level_required(4)
@admin.route('/themes/active')
def theme_active():
    Option.update('theme', request.args.get('theme'))
    fypress.options = Option.auto_load()
    return redirect(url_for('admin.themes'))

"""
    Settings
"""
@admin.route('/settings/all', methods=['POST', 'GET'])
@level_required(4)
def settings_general():
    form = GeneralSettingsForm(obj=Option.get_settings())

    if form.validate_on_submit():
        for data in form.data:
            Option.update(data, form.data[data])

        fypress.options = Option.auto_load()
        return redirect(url_for('admin.settings_general'))
        
    return render_template('admin/settings_general.html', form=form, title=gettext('General - Settings'))

@admin.route('/settings/social', methods=['POST', 'GET'])
@level_required(4)
def settings_social():
    form = SocialSettingsForm(obj=Option.get_settings('social'))

    if form.validate_on_submit():
        for data in form.data:
            Option.update(data, form.data[data])

        fypress.options = Option.auto_load()
        return redirect(url_for('admin.settings_social'))

    return render_template('admin/settings_social.html', form=form, title=gettext('Social - Settings'))


@admin.route('/settings/design', methods=['POST', 'GET'])
def settings_design():
    options = Option.get_settings('design')

    if request.form:
        for data in request.form:
            Option.update(data, request.form[data])

        fypress.options = Option.auto_load()
        return redirect(url_for('admin.settings_design'))

    return render_template('admin/settings_design.html', design=options, title=gettext('Design - Settings'))

@admin.route('/settings/reading')
def settings_reading():
    return render_template('admin/blank.html',  title=gettext('Design - Settings'))

'''
    Comments
'''
@admin.route('/comments', methods=['POST', 'GET'])
@admin.route('/comments/all', methods=['POST', 'GET'])
@level_required(4)
def comments():
    count_published = SimpleComment.count_filter(SimpleComment.status=='valid')
    count_spam      = SimpleComment.count_filter(SimpleComment.status=='spam')
    paginator = Paginator(
        query    = SimpleComment.filter(SimpleComment.status==(request.args.get('filter') or 'valid')).order_by(SimpleComment.created),
        page     = request.args.get('page')
    )
    akismet      = Option.get(Option.name=='akismet')

    if akismet:
        form = AkismetForm(api_key=akismet.value)
    else:
        form = AkismetForm()

    if form.validate_on_submit():
        Option.update('akismet', request.form['api_key'])
        fypress.options = Option.auto_load()
        return redirect(url_for('admin.comments'))

    return render_template('admin/comments.html', 
        count_published=count_published, 
        filter=request.args.get('filter'), 
        count_spam=count_spam, 
        pages=paginator.links,
        akismet=akismet,
        form=form,
        comments=paginator.items,
        title=gettext('Comments')
    )

@admin.route('/comments/delete')
def comments_delete():
    comment = SimpleComment.get(SimpleComment.id==request.args.get('id'))
    SimpleComment.count_comments(comment.id_post, True)
    comment.remove()
    
    return redirect(url_for('admin.comments'))

@admin.route('/comments/unspam')
def comments_unspam():
    comment = SimpleComment.get(SimpleComment.id==request.args.get('id'))
    comment.status = 'valid'
    comment.save()
    SimpleComment.count_comments(comment.id_post)

    return redirect(url_for('admin.comments'))

"""
    Posts & Pages
"""
@admin.route('/pages')
@admin.route('/pages/all')
@level_required(1)
def pages():
    return posts(True)

@admin.route('/pages/edit', methods=['POST', 'GET'])
@admin.route('/pages/new', methods=['POST', 'GET'])
@level_required(1)
def pages_add():
    return posts_add(True)

@admin.route('/posts')
@admin.route('/posts/all')
@level_required(1)
def posts(page=False):
    numbers = Post.count_by_status(page)
    if not request.args.get('filter'):
        query = Post.filter(Post.status << ['draft', 'published'], Post.type==('page' if page else 'post')).order_by(Post.created)
    else:
        query = Post.filter(Post.status==request.args.get('filter'), Post.type==('page' if page else 'post')).order_by(Post.created)

    if page:
        title = gettext('Page')
    else:
        title = gettext('Posts')

    paginator = Paginator(
        query    = query,
        page     = request.args.get('page')
    )

    if page: urls = 'admin.pages'
    else: urls = 'admin.posts'

    return render_template('admin/posts.html', pages=paginator.links, title=title, posts=paginator.items, numbers=numbers, filter=request.args.get('filter'), page=page, urls=urls)

@admin.route('/posts/delete')
@level_required(4)
def posts_delete():
    post = Post.get(Post.id==request.args.get('id'))
    if post:
        Post.delete(post)
        flash(messages['deleted']+' ('+str(post)+')')
        return redirect(get_redirect_target())
    else:
        return handle_404()

@admin.route('/posts/move')
@level_required(1)
def posts_move():
    post = Post.get(Post.id==request.args.get('id'))
    if post:
        post.move(request.args.get('status'))
        flash(messages['moved']+' to '+request.args.get('status')+' ('+str(post)+')')
        return redirect(get_redirect_target())
    else:
        return handle_404()

@admin.route('/posts/edit', methods=['POST', 'GET'])
@admin.route('/posts/new', methods=['POST', 'GET'])
@level_required(1)
def posts_add(page=False):
    post = False

    if page: urls = 'admin.pages'
    else: urls = 'admin.posts'

    if request.args.get('edit'):
        post = Post.get(Post.id==request.args.get('edit'))
        if post:
            if post.parent:
                return redirect(url_for(urls+'_add', edit=post.parent))
            if request.form:
                post = Post.update(request.form, post)
                flash(messages['updated']+' ('+str(post)+')')
                return redirect(url_for(urls+'_add', edit=post.id))
        else:
            return handle_404()
    else:
        if request.form:
            post = Post.new(request.form)
            flash(messages['added']+' ('+str(post)+')')
            return redirect(url_for(urls+'_add', edit=post.id))

    folders = Folder.get_all()

    if page:
        title = gettext('New - Page')
    else:
        title = gettext('New - Post')

    
    return render_template('admin/posts_new.html', folders=folders, post=post, title=title, page=page, urls=urls)

"""
    Medias
"""
@admin.route('/medias')
@admin.route('/medias/all')
@level_required(1)
def medias():
    if not request.args.get('filter'):
        query = Media.select().order_by(Media.modified)
    else:
        query = Media.filter(Media.type==request.args.get('filter')).order_by(Media.modified)

    paginator = Paginator(
        query    = query,
        page     = request.args.get('page'),
        per_page = 12
    )
    return render_template('admin/medias.html',  medias=paginator.items, pages=paginator.links, title=gettext('Library - Medias'))

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
        folder = Folder.get(Folder.id==request.args.get('edit'))
        form = FolderForm(obj=folder)
        if form.validate_on_submit():
            form.populate_obj(folder)
            folder.modified = datetime.datetime.now()
            folder.save()
            flash(messages['updated']+' ('+str(folder)+')')
            return redirect(url_for('admin.folders'))
    else:
        form = FolderForm()
        if form.validate_on_submit():
            Folder.add(form)
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
    paginator = Paginator(
        query    = User.select(),
        page     = request.args.get('page')
    )
    return render_template('admin/users.html', title=gettext('Users'), users=paginator.items, pages=paginator.links)

@admin.route('/users/edit', methods=['POST', 'GET'])
@level_required(0)
def users_edit(id_user=None):
    if not id_user:
        id_user = request.args.get('id')

    user = User.get(User.id==id_user)
    if g.user.status == 4:
        form = UserEditFormAdmin(obj=user)
    else:
        form = UserEditForm(obj=user)

    if form.validate_on_submit():
        status = user.status
        form.populate_obj(user)
        
        # don't allow to change status unless admin.
        if g.user.status != 4:
            user.status = status

        if g.user.status == 4 or g.user.id == user.id:
            user.save()
            flash(messages['updated']+' ('+str(user)+')')

        if g.user.status == 4:
            return redirect(url_for('admin.users'))
        else:
            return redirect(url_for('admin.users_me'))

    return render_template('admin/users_edit.html', title=gettext('Edit - User'), user=user, form=form)

@admin.route('/users/new', methods=['POST', 'GET'])
@level_required(4)
def users_new():
    form = UserAddForm(request.form)

    if form.validate_on_submit():
        user = User.create()
        form.populate_obj(user)
        user.save()
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
    media = Media.get(Media.id==request.args.get('id').replace('media_', ''))
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
    Folder.update_all(data)
    return ''