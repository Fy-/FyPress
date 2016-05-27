# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext as gettext
from fypress.utils import TreeHTML
from fypress.utils import slugify, url_unique
import fy_mysql, pprint

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

