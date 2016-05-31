# -*- coding: UTF-8 -*-

from fypress.utils import slugify, url_unique, TreeHTML
from fypress.utils import mysql

class Folder(mysql.Base):
    # /sql/folder.sql
    folder_id               = mysql.Column(etype='int', primary_key=True)
    folder_parent           = mysql.Column(etype='int')
    folder_left             = mysql.Column(etype='int')
    folder_right            = mysql.Column(etype='int')
    folder_depth            = mysql.Column(etype='int')
    folder_guid             = mysql.Column(etype='string', unique=True)
    folder_slug             = mysql.Column(etype='string', unique=True)
    folder_posts            = mysql.Column(etype='int')
    folder_name             = mysql.Column(etype='string', unique=True)
    folder_modified         = mysql.Column(etype='datetime')
    folder_created          = mysql.Column(etype='datetime')
    folder_content          = mysql.Column(etype='string')
    folder_seo_content      = mysql.Column(etype='string')

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
        folders = Folder.query.get_all(array=True)
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
        
        if not folders:
            return ''

        tree = TreeHTML(folders)
        return tree.generate_folders_admin(False, 'sortable')

