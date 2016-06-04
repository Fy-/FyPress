# -*- coding: UTF-8 -*-
from flask import Blueprint, url_for, render_template, request, make_response
from werkzeug.contrib.atom import AtomFeed
from fypress.admin import Option
from fypress.folder import Folder
from fypress.post import Post

public = Blueprint('public', __name__)

@public.route('/')
def root():
    return ''

@public.route('/feed/')
def feed():
  feed = AtomFeed(
    Option.get('name'),
    subtitle=Option.get('slogan'),
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
  return feed.get_response()

@public.route('/sitemap.xls')
def sitemap_xls():
  response = make_response(render_template('front/_sitemap.xls'))
  response.headers["Content-Type"] = 'application/xml'
  return response 

@public.route('/sitemap.xml')
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
      modified = folder.modified.isoformat()
      pages.append({'url': url, 'mod': modified, 'freq': 'weekly', 'prio': '0.6'})

  # pages
  posts = Post.query.filter(status='published', type='page').order_by('created').limit(20, 0, array=True)
  for post in posts:
      url      = request.url_root+post.guid+'/'
      modified = post.modified.isoformat()
      pages.append({'url': url, 'mod': modified, 'freq': 'monthly', 'prio': '0.9'})

  # posts
  posts = Post.query.filter(status='published', type='post').order_by('created').limit(20, 0, array=True)
  for post in posts:
      url      = request.url_root+post.guid+'/'
      modified = post.modified.isoformat()
      pages.append({'url': url, 'mod': modified, 'freq': 'monthly', 'prio': '0.8'})

  response = make_response(render_template('front/_sitemap.xml', pages=pages))
  response.headers["Content-Type"] = 'application/xml'
  return response 

