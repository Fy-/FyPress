# -*- coding: UTF-8 -*-
from flask import g, request
from werkzeug.utils import secure_filename
from fysql import CharColumn, TextColumn, BooleanColumn, DictColumn
from fypress.models import FyPressTables
from fypress.local import _fypress_
from fypress.folder import Folder
from fypress.post import Post

import os, imp

config      = _fypress_.config

class Theme(object):
    @staticmethod
    def get_template(key):
        key  = os.path.normpath(key)
        path = os.path.join(g.options['theme'], key)
        return path

    @staticmethod
    def get_template_static(key, file, config):
        key  = os.path.normpath(key)
        file = secure_filename(file)
        path = os.path.join(config.THEME_FOLDER, Theme.get_template(os.path.join('public', key)))
        return [path, file]

    @staticmethod
    def context():
        return dict(
            nav         = Theme._ctx_nav(), 
            theme       = Theme._ctx_theme,
            get_posts   = Theme._ctx_get_posts, 
            breadcrumb  = Theme._ctx_breadcrumb,
            is_home     = Theme._ctx_is_home(),
            title       = Theme._ctx_title,
            description = Theme._ctx_description,
            image       = Theme._ctx_image,
            options     = g.options,
            user        = g.user
        )

    @staticmethod
    def load_themes():
        themes = []

        for fn in os.listdir(config.THEME_FOLDER):
            file  = os.path.join(config.THEME_FOLDER, fn, 'theme.py')
            theme = imp.load_source(fn, file)

            themes.append(theme)
            
        return themes
    @staticmethod
    def _ctx_nav():
        nav = Folder.get_as_tree('nav', request.path)
        return nav

    @staticmethod
    def _ctx_is_home():
        is_home = False

        if request.url == g.options['url']:
            is_home = True

        return is_home     

    @staticmethod
    def _ctx_theme(v):
        return g.options['theme'] + '/' + v

    @staticmethod
    def _ctx_get_posts(order='post.created DESC', limit=5, type='post', folder=False):
        if not folder:
            return Post.filter(Post.status=='published', Post.type==type).order_by(order).limit(limit, 0)
        else:
            return Post.filter(Post.status=='published', Post.type==type, Post.id_folder==folder).order_by(order).limit(limit, 0)

    @staticmethod
    def _ctx_breadcrumb(item=False):
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

    @staticmethod
    def _ctx_title(item=False):
        if request.path == '/articles/':
            return 'Articles • '+g.options['name']
        elif isinstance(item, Folder):
            return item.name+' • '+g.options['name']
        elif isinstance(item, Post):
            if item.id_folder == 1:
                return item.title+' • '+g.options['name']
            return item.title+' • '+item.folder.name+' • '+g.options['name']
        return g.options['name']

    @staticmethod
    def _ctx_description(item=False):
        if request.path == '/articles/':
            return False
        elif isinstance(item, Folder):
            index = Post.filter(Post.id_folder==item.id, Post.slug=='index', Post.status=='published', Post.type=='page').one()
            if index:
                return index.get_excerpt(155)
            return item.seo_content
        elif isinstance(item, Post):
            return item.get_excerpt(155)
        else:
            return g.options['slogan']

    @staticmethod
    def _ctx_image(item=False):
        if request.path == '/articles/':
            return False
        elif isinstance(item, Folder):
            index = Post.filter(Post.id_folder==item.id, Post.slug=='index', Post.status=='published', Post.type=='page').one()
            if index and index.id_image != 0:
                return index.image
            return False
        elif isinstance(item, Post):
            if item.id_image != 0:
                return item.image

            index = Post.filter(Post.id_folder==item.id_folder, Post.slug=='index', Post.status=='published', Post.type=='page').one()
            if index and index.id_image != 0:
                return index.image
        
        return False    
class Option(FyPressTables):
    name  = CharColumn(pkey=True, unique=True, index=True, max_length=75)
    value = TextColumn()
    load  = BooleanColumn(index=True)

    @staticmethod
    def auto_load():
        final   = {}
        options = Option.filter(Option.load==1).all()
        for option in options:
            final[option.name] = option.value 

        return final

    @staticmethod
    def update(name, value, auto_load=1):
        option = Option.get(Option.name==name)
        if option:
            option.value = value
            option.save()
        else:
            option = Option.create(name=name, value=value, load=auto_load)

        return option

    @staticmethod
    def get_value(name):
        option = Option.get(Option.name==name)
        if option:
            return option.value
        return False

    @staticmethod
    def get_settings(option_type='general'):
        settings = {
            'general': ['name', 'url', 'slogan', 'footer'],
            'social' : ['analytics', 'twitter', 'facebook', 'github'],
            'design' : ['logo', 'ico', 'css']
        }

        class Result(object):
            """ wtform """
            def set(self, name, value):
                setattr(self, name, value)

        result  = Result()
        options = Option.filter(Option.name << settings[option_type]).all()
        for option in options:
            result.set(option.name, option.value)

        return result