# -*- coding: UTF-8 -*-
from flask import g, request
from flask_babel import lazy_gettext as gettext
from BeautifulSoup import *

from fypress.utils import slugify, url_unique
from fypress.folder import Folder
from fypress.user import User
from fypress.media import Media
from fypress.local import _fypress_
from fypress.models import FyPressTables
from fysql import CharColumn, DateTimeColumn, IntegerColumn, DictColumn, FKeyColumn, TextColumn

from akismet import Akismet

import datetime

config      = _fypress_.config
database    = _fypress_.database.db 

def slug_setter(value):
    return slugify(value)

class Post(FyPressTables):
    id_folder        = FKeyColumn(table=Folder, reference='folder')
    id_image         = FKeyColumn(table=Media, reference='image', required=False)
    id_user          = FKeyColumn(table=User, reference='user')
    parent           = IntegerColumn(index=True)
    guid             = CharColumn(index=True, max_length=255)
    modified         = DateTimeColumn(default=datetime.datetime.now)
    created          = DateTimeColumn(default=datetime.datetime.now)
    content          = TextColumn()
    title            = CharColumn(max_length=255)
    excerpt          = CharColumn(max_length=255)
    status           = CharColumn(max_length=20, index=True)
    comment_status   = CharColumn(max_length=20, index=True)
    comment_count    = IntegerColumn()
    slug             = CharColumn(index=True, max_length=255, setter=slug_setter)
    type             = CharColumn(index=True, max_length=50)
    views            = IntegerColumn()
    meta             = DictColumn()

    txt_to_status         = {
        'published' : gettext('Published'),
        'draft'     : gettext('Draft'),
        'trash'     : gettext('Deleted'),
        'revision'  : gettext('Revision')
    }

    @staticmethod
    def count_by_status(page=False):
        if page:
            add = 'AND type="page"'
        else:
            add = 'AND type="post"'

        query = """SELECT 
            (SELECT COUNT(*) FROM post WHERE status != 'revision' {0}) AS total ,
            (SELECT COUNT(*) FROM post WHERE status = 'published' {0}) AS published,
            (SELECT COUNT(*) FROM post WHERE status = 'draft' {0}) AS draft,
            (SELECT COUNT(*) FROM post WHERE status = 'trash' {0}) AS trash
        """.format(add)
        return database.raw(query).fetchone()

    @staticmethod
    def update(form, post):
        status = 'draft'

        if request.args.get('action') == 'publish':
            status = 'published'
            if post.status != 'published':
                post.created = datetime.datetime.now()
        if request.args.get('action') == 'draft':
            status = 'draft'

        slug = form['title']
        if form.has_key('slug'):
            slug = form['slug']

        post.title          = form['title']
        post.content        = form['content']
        post.id_folder      = form['folder']
        post.modified       = datetime.datetime.now()
        post.status         = status
        post.excerpt        = post.get_excerpt()
        post.slug           = slug
        post.guid           = post.guid_generate()
        post.id_image       = form['image']
        post.save()

        post = Post.get(Post.id==post.id)
        post_id = post.id

        #if post.status == 'published':
        #    post.create_revision()

        post.folder.count_posts()

        return post

    @staticmethod
    def new(form):
        # Todo: create post, add_revision, update folder count.
        status = 'draft'
        if request.args.get('action') == 'publish':
            status = 'published'

        slug = form['title']
        if form.has_key('slug'):
            slug = form['slug']

        post = Post()
        post.title          = form['title']
        post.content        = form['content']
        post.id_folder      = form['folder']
        post.id_user        = g.user.id
        post.parent         = 0
        post.excerpt        = post.get_excerpt()
        post.status         = status
        post.comment_status = 'open'
        post.comment_count  = 0
        post.slug           = slug
        post.guid           = post.guid_generate()
        post.id_image       = form['image']
        post.type           = form['type']

        post = post.insert()
        post.folder.count_posts()

        post_id = post.id
        
        #if post.status == 'published':
        #    post.create_revision()

        return post

    def create_revision(self):
        """
        post        = self
        post.parent = post.id
        post.id     = ''
        post.guid   = post.guid_generate(rev=post.parent)
        post.status = 'revision'
        Post.query.add(post)
        return True
        """
        pass

    def guid_generate(self, rev=False):
        count = ''
        if rev:
            count = Post.filter(Post.parent==rev).all()
            count = '&rev='+str(len(count))
            return '?post_id={}'.format(rev)+count

        path = Folder.get(Folder.id == self.id_folder)
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
        soup = Post.excerpt_utils_rm_headers(BeautifulSoup(self.content))
        text = ''.join(soup.findAll(text=True)).split('\n')
        return ' '.join(text).strip()[0:size]   
    
    @staticmethod
    def excerpt_utils_rm_headers(soup):
        [[tree.extract() for tree in soup(elem)] for elem in ('h1','h2','h3','h4','h5','h6')]
        return soup

    def count_revs(self):
        return Post.count_filter(Post.parent==self.id)

    def move(self, status='draft'):
        self.status = status
        self.save()

        return self.id

    @staticmethod
    def delete(post):
        childs = Post.filter(Post.parent==post.id).all()
        for post in childs:
            post.remove()

        self.remove()

    @staticmethod
    def link_posts():
        posts = Post.filter(Post.status << ['draft', 'published', 'trash']).all()
        for post in posts:
            post.guid = post.guid_generate()
            post.save()

class Comment(FyPressTables):
    id_user          = FKeyColumn(table=User, reference='user')
    id_post          = FKeyColumn(table=Post, reference='post')
    parent           = IntegerColumn(index=True)
    created          = DateTimeColumn(default=datetime.datetime.now)
    content          = TextColumn()
    status           = CharColumn(max_length=20, index=True)
    user_name        = CharColumn(max_length=75) 
    user_uri         = CharColumn(max_length=150)
    user_email       = CharColumn(max_length=150) 
    user_ip          = CharColumn(max_length=30)

    @property
    def uri(self):
        if self.user_id != 0:
            return self.user.url
        else:
            return self.user_uri

    @property
    def author(self):
        if self.user_id != 0:
            return self.user.nicename
        else:
            return self.user_name

    @property
    def email(self):
        if self.user_id != 0:
            return self.user.email
        else:
            return self.user_email

    def gravatar(self, size=50):
        default = "identicon"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url

    @staticmethod
    def check(comment):
        from fypress.admin import Option
        if False: #check akismetapikey, ip= request.remote_addr
            akismet = Akismet('1ba29d6f120c', blog=Options.get('url'), user_agent=request.headers.get('User-Agent'))
            rv = akismet.check(
                comment.ip, 
                request.headers.get('User-Agent'), 
                comment_author=comment.author,
                comment_author_email=comment.email, 
                comment_author_url=comment.uri,
                comment_content=comment.content
            )

            print rv
