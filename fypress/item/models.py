# -*- coding: UTF-8 -*-
from flask import jsonify
from flask.ext.babel import lazy_gettext as gettext
from werkzeug import secure_filename
import hashlib, os, datetime, shutil, magic, json

from fypress import app
from fypress.utils import TreeHTML, slugify, url_unique, oembed, FyImage
import fy_mysql

class Media(fy_mysql.Base):
    # todo allowed {type, icon, }
    allowed_upload_types  = ('image/jpeg', 'image/png', 'image/gif')
    upload_types_images   = ('image/jpeg', 'image/png')

    media_id              = fy_mysql.Column(etype='int', primary_key=True)
    media_hash            = fy_mysql.Column(etype='string', unique=True)
    media_modified        = fy_mysql.Column(etype='datetime')
    media_type            = fy_mysql.Column(etype='string')
    media_guid            = fy_mysql.Column(etype='string', unique=True)
    media_name            = fy_mysql.Column(etype='string')
    media_data            = fy_mysql.Column(etype='json')
    media_icon            = fy_mysql.Column(etype='string')
    media_html            = fy_mysql.Column(etype='string')
    media_childs          = fy_mysql.Column(childs=True)

    def generate_html(self):
        pass

    def urlify(self, image=False):
        if image:
            try:
                return app.config['UPLOAD_DIRECTORY_URL'] + self.data['var'][image]['guid']
            except:
                return ''
        else:
            return app.config['UPLOAD_DIRECTORY_URL'] + self.guid

    @staticmethod
    def add_from_web(url):
        oembed_ = oembed().get(url) 

        return jsonify(result=oembed_)

    @staticmethod
    def upload_path(config):
        now = datetime.datetime.now()
        tmp = "{}/{}".format(now.year, now.month)
        if config == 'CHUNKS_DIRECTORY':
            return os.path.join(app.config[config])
        return os.path.join(app.config[config], tmp)

    @staticmethod
    def upload_save(f, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, 'wb+') as destination:
            destination.write(f.stream.read())

    @staticmethod
    def upload_combine_chunks(total_parts, total_size, source_folder, dest):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        with open(dest, 'wb+') as destination:
            for i in xrange(int(total_parts)):
                part = os.path.join(source_folder, str(i))
                with open(part, 'rb') as source:
                    destination.write(source.read())
    @staticmethod
    def upload(file, attrs):        
        fhash   = attrs['qquuid']
        upload_type = 'file'
        upload_icon = 'fa-file-o'
        filename = url_unique(secure_filename(attrs['qqfilename']), Media)

        chunked = False

        fdir    = Media.upload_path('UPLOAD_DIRECTORY')
        fpath   = os.path.join(fdir, filename)
        

        if attrs.has_key('qqtotalparts') and int(attrs['qqtotalparts']) > 1:
            chunked = True
            fdir    = Media.upload_path('CHUNKS_DIRECTORY')
            fpath   = os.path.join(fdir, filename, str(attrs['qqpartindex']))

        Media.upload_save(file, fpath)

        if chunked and (int(attrs['qqtotalparts']) - 1 == int(attrs['qqpartindex'])):
            Media.upload_combine_chunks(attrs['qqtotalparts'], attrs['qqtotalfilesize'], os.path.dirname(fpath), os.path.join(Media.upload_path('UPLOAD_DIRECTORY'), filename))
            shutil.rmtree(os.path.dirname(os.path.dirname(fpath)))

        mime = magic.Magic(mime=True)
        mime_file = mime.from_file(os.path.join(Media.upload_path('UPLOAD_DIRECTORY'), filename))

        if mime_file not in Media.allowed_upload_types:
            os.remove(os.path.join(Media.upload_path('UPLOAD_DIRECTORY'), filename))
            return jsonify(success=False, error='File type not allowed.'), 400

        if mime_file in Media.upload_types_images:
             upload_type = 'image'
             upload_icon = ' fa-file-image-o'

        media_hash = Media.hash_file(fpath)
        if Media.query.exist('hash', media_hash):
            media = Media.query.filter(hash=media_hash).one()
            media.modified = 'NOW()'
            Media.query.update(media)

            return jsonify(success=True), 200

        now = datetime.datetime.now()
        media = Media()
        media.hash          = media_hash
        media.modified      = 'NOW()'
        media.type          = upload_type
        media.name          = filename
        media.guid          = "{}/{}/".format(now.year, now.month)+filename
        media.source        = fpath
        media.icon          = upload_icon

        Media.query.add(media)

        if upload_type == 'image':
            images = FyImage(fpath).generate()
            sizes = {}

            for image in images:
                sizes[image[3]] = {'name': image[1], 'source': os.path.join(Media.upload_path('UPLOAD_DIRECTORY'), image[0]), 'guid': "{}/{}/".format(now.year, now.month)+image[2]}

            media.data = {'var':sizes}
            Media.query.update(media)

        return jsonify(success=True), 200

    @staticmethod
    def hash_string(txt):
        hasher = hashlib.sha1()
        hasher.update(txt)
        return hasher.hexdigest() 

    @staticmethod
    def hash_file(file):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()

        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)

        return hasher.hexdigest()

class Post(fy_mysql.Base):
    post_id               = fy_mysql.Column(etype='int', primary_key=True)
    post_folder           = fy_mysql.Column(etype='int') 
    post_user_id          = fy_mysql.Column(etype='int')
    post_parent           = fy_mysql.Column(etype='int')
    post_guid             = fy_mysql.Column(etype='string', unique=True)
    post_modified         = fy_mysql.Column(etype='datetime')
    post_created          = fy_mysql.Column(etype='datetime')
    post_content          = fy_mysql.Column(etype='string')
    post_title            = fy_mysql.Column(etype='string')
    post_excerpt          = fy_mysql.Column(etype='string')
    post_status           = fy_mysql.Column(etype='string', allowed=('publish','draft','pending','trash','inherit')) 
    post_comment_status   = fy_mysql.Column(etype='string', allowed=('open', 'close')) 
    post_comment_count    = fy_mysql.Column(etype='int')
    post_slug             = fy_mysql.Column(etype='string', unique=True)
    post_type             = fy_mysql.Column(etype='string')
    post_meta             = fy_mysql.Column(meta=True)

    def create(self):
        # Todo: create post, add_revision, update folder count.
        pass

    def update(self):
        pass

    def move(self):
        pass

    def add_revision(self):
        pass

    def get_revisions(self):
        pass

    def delete(self):
        pass

    def get_uid(self):
        pass

    def get_folders(self):
        pass

class Folder(fy_mysql.Base):
    # /sql/folder.sql
    folder_id               = fy_mysql.Column(etype='int', primary_key=True)
    folder_parent           = fy_mysql.Column(etype='int')
    folder_left             = fy_mysql.Column(etype='int')
    folder_right            = fy_mysql.Column(etype='int')
    folder_depth            = fy_mysql.Column(etype='int')
    folder_guid             = fy_mysql.Column(etype='string', unique=True)
    folder_slug             = fy_mysql.Column(etype='string', unique=True)
    folder_posts            = fy_mysql.Column(etype='int')
    folder_name             = fy_mysql.Column(etype='string', unique=True)
    folder_modified         = fy_mysql.Column(etype='datetime')
    folder_created          = fy_mysql.Column(etype='datetime')
    folder_content          = fy_mysql.Column(etype='string')
    folder_seo_content      = fy_mysql.Column(etype='string')

    @property
    def slug(self):
        if self.__dict__.has_key('slug'):
            return self.__dict__['slug']

    @slug.setter
    def slug(self, value):
        self.__dict__['slug'] = slugify(value)


    def update(self):
        Folder.query.update(self)
        self.build_guid()

    def update_guid(self):
        query = """
          SELECT
            GROUP_CONCAT(parent.folder_slug SEPARATOR '/') AS path
          FROM
            fypress_folder AS node,
            fypress_folder AS parent
          WHERE
            node.folder_left BETWEEN parent.folder_left AND parent.folder_right AND node.folder_id={0}
          ORDER BY
            parent.folder_left""".format(self.id)

        self.guid = url_unique(Folder.query.raw(query).one()[0]['path'], Folder, self.id)

        Folder.query.update(self)

    @staticmethod
    def build_guid():
        folders = Folder.query.get_all()
        for folder in folders:
            folder.update_guid()

    @staticmethod
    def get_all(html = False):
        query = """
            SELECT
                node.folder_seo_content,
                node.folder_created,
                node.folder_modified,
                node.folder_parent,
                node.folder_name,
                node.folder_depth,
                node.folder_posts,
                node.folder_id,
                node.folder_left,
                node.folder_content,
                node.folder_slug,
                node.folder_right
            FROM
                fypress_folder AS node,
                fypress_folder AS parent
            WHERE
                node.folder_left BETWEEN parent.folder_left AND parent.folder_right
            GROUP BY
                node.folder_id
            ORDER BY
                node.folder_left, node.folder_id
        """


        folders = Folder.query.sql(query).all(array=True)
        
        if not html:
            return folders
            
        tree = TreeHTML(folders)
        return tree.generate_folders_admin(False, 'sortable')

