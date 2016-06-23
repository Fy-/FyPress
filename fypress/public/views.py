# -*- coding: UTF-8 -*-
from flask import Blueprint, url_for, render_template, request, make_response, g, send_from_directory, redirect, session
from werkzeug.contrib.atom import AtomFeed
from fypress.local import _fypress_
from fypress.folder import Folder
from fypress.post import Post
from fypress.admin import Option, Theme
from fypress.utils import Paginator
from fypress.folder import Folder
from fypress.user import User
from fypress.admin.views import handle_404 as is_admin_404
from fypress import __version__

from .decorators import cached

public  = Blueprint('public', __name__)
config  = _fypress_.config

def is_404():
    return render_template(Theme.get_template('404.html')), 404

@public.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.get(User.id==session['user_id'])

    g.options = Option.auto_load()

@public.context_processor
def template():
    return Theme.context()

@public.route('/')
@cached(pretty=True)
def root():
    index = Post.filter(Post.id_folder==1, Post.slug=='index', Post.status=='published', Post.type=='page').one()
    return render_template(Theme.get_template('index.html'), index=index, this=False)

@public.route('/_preview/')
def preview():
    g.options['theme'] = request.args.get('theme')
    return root()

@public.route('/articles/')
@cached(pretty=True)
def posts():
    folder = Folder()
    folder.name = 'Articles'
    folder.guid = 'articles'
    folder.is_folder = True
    folder.posts     = Paginator(
            query    = Post.filter(Post.status=='published', Post.type=='post').order_by(Post.created, 'DESC'),
            page     = request.args.get('page'),
            theme    = 'bootstrap',
            per_page = 6
    )
    return render_template(Theme.get_template('articles.html'), this=folder)

@public.route('/<path:slug>.html')
@cached(pretty=True)
def is_post(slug):
    post = Post.get(Post.guid==slug)
    if post:
        if post.slug == 'index' and post.id_folder != 0:
            return redirect('/'+post.folder.guid+'/')

        post.views += 1
        post.save()
        
        if post.type == 'post':
            post.is_post = True
            return render_template(Theme.get_template('post.html'), this=post, show_sidebar=False)
        else:
            post.is_page = True
            post.pages = Post.filter(Post.id_folder==post.id_folder, Post.status=='published', Post.type=='page').order_by(Post.created).all()
            return render_template(Theme.get_template('page.html'), this=post)
    else:
        return is_404()
    
@public.route('/<path:slug>/')
@cached(pretty=True)
def is_folder(slug):
    if slug.split('/')[0] != 'admin':
        folder = Folder.get(Folder.guid==slug)
        if folder:
            folder.is_folder    = True
            folder.pages        = Post.filter(Post.id_folder==folder.id, Post.status=='published', Post.type=='page').order_by(Post.created).all()
            folder.index        = Post.filter(Post.id_folder==folder.id, Post.slug=='index', Post.status=='published', Post.type=='page').one()
            folder.posts        = Paginator(
                query    = Post.filter(Post.id_folder==folder.id, Post.status=='published', Post.type=='post').order_by(Post.created),
                page     = request.args.get('page'),
                theme    = 'bootstrap',
                per_page = 5
            )

            return render_template(Theme.get_template('folder.html'), this=folder)
        else:
            return is_404()
    else:
        return is_admin_404()

@public.route('/public/<path:folder>/<file>')
def static(folder, file):
    folder, file = Theme.get_template_static(folder, file, config)
    return send_from_directory(folder, file)

@public.route('/feed/<path:folder>/')
@cached()
def feed_folder(folder):
    if folder.split('/')[0] != 'admin':
        folder = Folder.get(Folder.guid==folder)
        if folder:
            posts = Post.filter(Post.id_folder==folder.id, Post.status=='published', Post.type=='post').order_by(Post.created).limit(20)

            feed = AtomFeed(
                g.options['name']+' • ' + folder.name,
                subtitle=folder.seo_content,
                feed_url=request.url_root+'feed/',
                url=request.url_root,
                generator=None
            )

            for post in posts:
                feed.add(
                    post.title, 
                    post.content,
                    content_type='html',
                    author=post.user.nicename,
                    url=request.url_root+post.guid,
                    updated=post.modified,
                    published=post.created
                )


            response = feed.get_response()
            response.headers["Content-Type"] = 'application/xml'

            return response
        else:
            return is_404()
    else:
        return is_admin_404()

@public.route('/feed/')
@cached()
def feed():

    feed = AtomFeed(
        g.options['name'],
        subtitle=g.options['slogan'],
        feed_url=request.url_root+'feed/',
        url=request.url_root,
        generator=None
    )

    posts = Post.filter(Post.status=='published', Post.type=='post').order_by(Post.created).limit(20)
    for post in posts:
        feed.add(
            post.title, 
            post.content,
            content_type='html',
            author=post.user.nicename,
            url=request.url_root+post.guid,
            updated=post.modified,
            published=post.created
        )


    response = feed.get_response()
    response.headers["Content-Type"] = 'application/xml'

    return response

@public.route('/sitemap.xls')
@cached()
def sitemap_xls():
    response = make_response(render_template(Theme.get_template('_sitemap.xls')))
    response.headers["Content-Type"] = 'application/xml'
    return response 

@public.route('/sitemap.xml')
@cached()
def sitemap():
    posts   = Post.filter(Post.status=='published', Post.type=='post').order_by(Post.created).all()
    folders = Folder.get_all()

    pages = []

    # home
    pages.append({'url': request.url_root, 'freq': 'daily', 'prio': '1'})

    # folders
    for folder in folders:
        if folder.guid != '':
            url      = request.url_root+folder.guid+'/'
            modified = folder.modified.strftime('%Y-%m-%d')
            pages.append({'url': url, 'mod': modified, 'freq': 'weekly', 'prio': '0.6'})

    # pages
    posts = Post.filter(Post.status=='published', Post.type=='page').order_by(Post.created).limit(20)
    for post in posts:
            if post.slug != 'index':
                url      = request.url_root+post.guid+'.html'
                modified = post.modified.strftime('%Y-%m-%d')
                pages.append({'url': url, 'mod': modified, 'freq': 'monthly', 'prio': '0.9'})

    # posts
    posts = Post.filter(Post.status=='published', Post.type=='post').order_by(Post.created).limit(20,)
    for post in posts:
            url      = request.url_root+post.guid+'.html'
            modified = post.modified.strftime('%Y-%m-%d')
            pages.append({'url': url, 'mod': modified, 'freq': 'monthly', 'prio': '0.8'})

    response = make_response(render_template(Theme.get_template('_sitemap.xml'), pages=pages))
    response.headers["Content-Type"] = 'application/xml'
    return response 