# -*- coding: UTF-8 -*-
from flask import g, request
from flask.ext.babel import lazy_gettext as gettext
from BeautifulSoup import *

from fypress.utils import slugify, url_unique
from fypress.folder import Folder
from fypress.user import User
from fypress.media import Media
from fypress.utils import mysql

class Post(mysql.Base):
    post_id               = mysql.Column(etype='int', primary_key=True)
    post_folder_id        = mysql.Column(etype='int') 
    post_image_id         = mysql.Column(etype='int') 
    post_user_id          = mysql.Column(etype='int')
    post_parent           = mysql.Column(etype='int')
    post_guid             = mysql.Column(etype='string', unique=True)
    post_modified         = mysql.Column(etype='datetime')
    post_created          = mysql.Column(etype='datetime')
    post_content          = mysql.Column(etype='string')
    post_title            = mysql.Column(etype='string')
    post_excerpt          = mysql.Column(etype='string')
    post_status           = mysql.Column(etype='string') 
    post_comment_status   = mysql.Column(etype='string') 
    post_comment_count    = mysql.Column(etype='int')
    post_slug             = mysql.Column(etype='string', unique=True)
    post_type             = mysql.Column(etype='string')
    post_meta             = mysql.Column(meta=True)
    post_folder           = mysql.Column(object=Folder, link='folder_id')
    post_image            = mysql.Column(object=Media, link='image_id')
    post_user             = mysql.Column(object=User, link='user_id')

    txt_to_status         = {
        'published' : gettext('Published'),
        'draft'     : gettext('Draft'),
        'trash'     : gettext('Deleted'),
        'revision'  : gettext('Revision')
    }

    @property
    def slug(self):
        if self.__dict__.has_key('slug'):
            return self.__dict__['slug']

    @slug.setter
    def slug(self, value):
        self.__dict__['slug'] = slugify(value)

    @staticmethod
    def count_by_status(page=False):
        if page:
            add = 'AND post_type="page"'
        else:
            add = 'AND post_type="post"'

        query = """SELECT 
            (SELECT COUNT(*) FROM fypress_post WHERE post_status != 'revision' {0}) AS total ,
            (SELECT COUNT(*) FROM fypress_post WHERE post_status = 'published' {0}) AS published,
            (SELECT COUNT(*) FROM fypress_post WHERE post_status = 'draft' {0}) AS draft,
            (SELECT COUNT(*) FROM fypress_post WHERE post_status = 'trash' {0}) AS trash
        """.format(add)

        return Post.query.raw(query).result()[0]

    @staticmethod
    def update(form, post):
        status = 'draft'

        if request.args.get('action') == 'publish':
            status = 'published'
            post.created = 'NOW()'
        if request.args.get('action') == 'draft':
            status = 'draft'

        slug = form['title']
        if form.has_key('slug'):
            slug = form['slug']

        post.title          = form['title']
        post.content        = form['content']
        post.folder_id      = form['folder']
        post.modified       = 'NOW()'
        post.status         = status
        post.excerpt        = post.get_excerpt()
        post.slug           = slug
        post.guid           = post.guid_generate()
        post.image_id  = form['image']
        Post.query.update(post)
        post_id = post.id
        if post.status == 'published':
            post.create_revision()

        post.folder.count_posts()

        return post_id

    @staticmethod
    def create(form):
        # Todo: create post, add_revision, update folder count.
        status = 'draft'
        if request.args.get('action') == 'publish':
            status = 'published'

        slug = form['title']
        if form.has_key('slug'):
            slug = form['slug']

        post = Post()
        post.id             = None
        post.title          = form['title']
        post.content        = form['content']
        post.folder_id      = form['folder']
        post.user_id        = g.user.id
        post.parent         = 0
        post.modified       = 'NOW()'
        post.created        = 'NOW()'
        post.excerpt        = post.get_excerpt()
        post.status         = status
        post.comment_status = 'open'
        post.comment_count  = 0
        post.slug           = slug
        post.guid           = post.guid_generate()
        post.image_id       = form['image']
        post.type           = form['type']

        Post.query.add(post)
        post.folder.count_posts()

        post_id = post.id
        if post.status == 'published':
            post.create_revision()

        return post_id

    def create_revision(self):
        post        = self
        post.parent = post.id
        post.id     = ''
        post.guid   = post.guid_generate(rev=post.parent)
        post.status = 'revision'
        Post.query.add(post)
        return True

    def guid_generate(self, rev=False):
        count = ''
        if rev:
            count = Post.query.filter(parent=rev).all(array=True)
            count = '&rev='+str(len(count))
            return '?post_id={}'.format(rev)+count

        path = Folder.query.get(self.folder_id)
        path = path.guid
        name = self.slug + count
        
        if self.id:
            guid = url_unique(path+'/'+name, Post, self.id)
        else:
            guid = url_unique(path+'/'+name, Post)

        if guid[0] == '/':
            guid = guid[1:]

        return guid


    def get_excerpt(self, size=255):
        # https://github.com/dziegler/excerpt_extractor/tree/master

        soup = Post.except_utils_rm_headers(BeautifulSoup(self.content))
        text = ''.join(soup.findAll(text=True)).split('\n')
        description = max((len(i.strip()),i) for i in text)[1].strip()[0:size]
        return description   
    
    @staticmethod
    def except_utils_rm_headers(soup):
        [[tree.extract() for tree in soup(elem)] for elem in ('h1','h2','h3','h4','h5','h6')]
        return soup

    def count_revs(self):
        return Post.query.count(parent=self.id)

    def move(self, status='draft'):
        self.status = status
        Post.query.update(self)

        return self.id

    @staticmethod
    def delete(post):
        childs = Post.query.filter(parent=post.id).all(array=True)
        for post in childs:
            Post.query.delete(post)

        Post.query.delete(post)
