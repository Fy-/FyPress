# -*- coding: UTF-8 -*-
from flask import Blueprint, url_for, render_template, request, make_response, g, send_from_directory, redirect, session
from werkzeug.contrib.atom import AtomFeed
from fypress.local import _fypress_
from fypress.folder import Folder
from fypress.post import Post, get_posts
from fypress.admin import Option
from fypress.utils import get_template, get_template_static, Paginator
from fypress.folder import Folder
from fypress.admin.views import handle_404 as is_admin_404
from .decorators import cached

public  = Blueprint('public', __name__)
options = []
user    = None
config  = _fypress_.config

def is_404():
    return render_template(get_template('404.html', config)), 404

def reset_options():
    global options
    options = []

@public.context_processor
def inject_options():
    if '/public/' not in request.path:
        from fypress.utils.mysql.sql import FyMySQL
        from fypress import __version__

        return dict(options=g.options, queries=FyMySQL._instance.queries, version=__version__, debug=config.DEBUG)

@public.before_request
def before_request():
    global options

    if '/public/' not in request.path:
        from fypress.user import User
        g.user = None
        if 'user_id' in session:
            g.user = User.query.get(session['user_id'])
        

    if len(options) == 0:
        from fypress.admin import Option
        options = Option.auto_load()

    g.options = options

@public.context_processor
def template():
    nav = Folder.get_as_tree('nav', request.path)
    is_home = False

    if request.url == g.options['url']:
        is_home = True

    def breadcrumb(item=False):
        if request.path == '/articles/':
            folder = Folder()
            folder.name = 'Articles'
            folder.guid = 'articles'
            return [folder]
        elif item:
            if isinstance(item, Folder):
                return item.get_path(item)
            elif isinstance(item, Post):
                return item.folder.get_path(item.folder)
        return []

    def title(item=False):
        if request.path == '/articles/':
            return 'Articles • '+g.options['name']
        elif isinstance(item, Folder):
            return item.name+' • '+g.options['name']
        elif isinstance(item, Post):
            return item.title+' • '+g.options['name']
        return g.options['name']

    def description(item=False):
        if request.path == '/articles/':
            return ''
        elif isinstance(item, Folder):
            index = Post.query.filter(folder_id=item.id, slug='index', status='published', type='page').one()
            if index:
                return index.get_excerpt(155)
            return item.seo_content
        elif isinstance(item, Post):
            return item.get_excerpt(155)
        else:
            return g.options['slogan']

    def seo(item=False):
        pass

    return dict(
        nav=nav, 
        get_posts=get_posts, 
        show_sidebar=True,
        show_breadcrumb=True, 
        show_footer=True,
        breadcrumb=breadcrumb,
        is_home=is_home,
        title=title,
        description=description
    )

@public.route('/')
@cached(pretty=True)
def root():
    index = Post.query.filter(folder_id=1, slug='index', status='published', type='page').one()
    return render_template(get_template('index.html', config), index=index)

@public.route('/<path:slug>.html')
@cached(pretty=True)
def is_post(slug):
    post = Post.query.filter(guid=slug).one()
    if post:
        if post.slug == 'index' and post.folder_id != 0:
            return redirect('/'+post.folder.guid+'/')

        post.views += 1
        Post.query.update(post)
        if post.type == 'post':
            return render_template(get_template('post.html', config), post=post, show_sidebar=False)
        else:
            pages = Post.query.filter(folder_id=post.folder_id, status='published', type='page').order_by('created').all(array=True)
            return render_template(get_template('page.html', config), page=post, pages=pages)
    else:
        return is_404()
    

@public.route('/articles/')
@cached(pretty=True)
def posts():
    folder = Folder()
    folder.name = 'Articles'
    folder.guid = 'articles'

    articles = Paginator(
            query    = Post.query.filter(status='published', type='post').order_by('created', 'DESC'),
            page     = request.args.get('page'),
            theme    = 'foundation',
            per_page = 2
    )
    return render_template(get_template('articles.html', config), paginator=articles, articles=articles, folder=folder)

@public.route('/<path:slug>/')
@cached(pretty=True)
def is_folder(slug):
    if slug.split('/')[0] != 'admin':
        folder = Folder.query.filter(guid=slug).one()
        if folder:
            articles = Paginator(
                    query    = Post.query.filter(folder_id=folder.id, status='published', type='post').order_by('created'),
                    page     = request.args.get('page')
            )

            pages = Post.query.filter(folder_id=folder.id, status='published', type='page').order_by('created').all(array=True)
            index = Post.query.filter(folder_id=folder.id, slug='index', status='published', type='page').one()

            return render_template(get_template('folder.html', config), folder=folder, paginator=articles, articles=articles, pages=pages, index=index)
        else:
            return is_404()
    else:
        return is_admin_404()

@public.route('/public/<path:folder>/<file>')
def static(folder, file):
    folder, file = get_template_static(folder, file, config)
    return send_from_directory(folder, file)

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

    posts = Post.query.filter(status='published', type='post').order_by('created').limit(20, 0, array=True)
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
    response = make_response(render_template('front/_sitemap.xls'))
    response.headers["Content-Type"] = 'application/xml'
    return response 

@public.route('/sitemap.xml')
@cached()
def sitemap():
    posts   = Post.query.filter(status='published', type='post').order_by('created').all()
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
    posts = Post.query.filter(status='published', type='page').order_by('created').limit(20, 0, array=True)
    for post in posts:
            if post.slug != 'index':
                url      = request.url_root+post.guid+'.html'
                modified = post.modified.strftime('%Y-%m-%d')
                pages.append({'url': url, 'mod': modified, 'freq': 'monthly', 'prio': '0.9'})

    # posts
    posts = Post.query.filter(status='published', type='post').order_by('created').limit(20, 0, array=True)
    for post in posts:
            url      = request.url_root+post.guid+'.html'
            modified = post.modified.strftime('%Y-%m-%d')
            pages.append({'url': url, 'mod': modified, 'freq': 'monthly', 'prio': '0.8'})

    response = make_response(render_template('front/_sitemap.xml', pages=pages))
    response.headers["Content-Type"] = 'application/xml'
    return response 