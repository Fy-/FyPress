# -*- coding: UTF-8 -*-
from fypress.utils import slugify, url_unique, TreeHTML
from fypress.utils import mysql
from fypress.local import _fypress_
config = _fypress_.config


class Folder(mysql.Base):
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

    def count_posts(self):
        query = """
            UPDATE
              {0}folder
            SET
              {0}folder.folder_posts =(
                  SELECT
                    COUNT(*)
                  FROM
                    {0}post
                  WHERE
                    {0}post.post_parent = 0 AND {0}post.post_folder_id = {0}folder.folder_id
            )
        """.format(config.MYSQL_PREFIX)
        Folder.query.sql(query).execute()

    @staticmethod
    def update_all(data):
        if data:
            exist = []
            for item in data:
                if item.has_key('id') and item['id'] != '1':
                    exist.append(int(item['id']))
                    folder = Folder.query.get(item['id'])
                    folder.depth    = item['depth']
                    folder.left     = item['left']
                    folder.right    = item['right']
                    folder.parent   = item['parent_id']

                    folder.modified = 'NOW()'
                    Folder.query.update(folder)

            all_folders = []
            folders = Folder.query.get_all(array=True)
            for folder in folders:
                all_folders.append(int(folder.id))

            diff = [item for item in all_folders if item not in exist]
            for item in diff:
                if item != 1:
                    from fypress.post import Post 
                    posts = Post.query.filter(folder_id=item).all(array=True)
                    for post in posts:
                        post.folder_id = 1
                        Post.query.update(post)
                    Folder.query.delete(Folder.query.get(item))

            for folder in folders:
                folder.count_posts()

            Folder.build_guid()
            from fypress.post import Post
            
            Post.link_posts()        

    @staticmethod
    def update_guid(folder):
        query = """
          SELECT
            GROUP_CONCAT(parent.folder_slug SEPARATOR '/') AS path
          FROM
            {1}folder AS node,
            {1}folder AS parent
          WHERE
            node.folder_left BETWEEN parent.folder_left AND parent.folder_right AND node.folder_id={0} AND node.folder_id!=1
          ORDER BY
            parent.folder_left""".format(folder.id, config.MYSQL_PREFIX)

        folder.guid = url_unique(Folder.query.raw(query).one()[0]['path'], Folder, folder.id)

        Folder.query.update(folder)

    @staticmethod
    def build_guid():
        folders = Folder.query.get_all(array=True)
        for folder in folders:
            Folder.update_guid(folder)

    @staticmethod
    def add(form):
        query = """
            SELECT MAX(folder_left) as l, MAX(folder_right) as r
            FROM {0}folder
        """.format(config.MYSQL_PREFIX)
        
        rv = Folder.query.raw(query).one()[0]
        if rv['r'] == 0 and rv['l'] == 0:
            rv['r'] = 1

        folder = Folder()
        form.populate_obj(folder)
        folder.created = 'NOW()'
        folder.parent  = 1
        folder.left    = rv['r']+1
        folder.right   = rv['r']+2
        Folder.query.add(folder)
        Folder.build_guid()

    @staticmethod
    def get_path(folder):
        query = """
          SELECT
            parent.folder_seo_content, parent.folder_created, parent.folder_modified, parent.folder_parent, parent.folder_content, parent.folder_name, parent.folder_left, parent.folder_id, parent.folder_guid, parent.folder_posts, parent.folder_slug, parent.folder_depth, parent.folder_right
          FROM
            {1}folder AS node,
            {1}folder AS parent
          WHERE
            node.folder_left BETWEEN parent.folder_left AND parent.folder_right AND node.folder_id={0} AND node.folder_id!=1
          ORDER BY
            parent.folder_left

           """.format(folder.id, config.MYSQL_PREFIX)


        return Folder.query.sql(query).all(array=True)



    @staticmethod
    def get_as_tree(mode='nav', current=''):
        folders = Folder.get_all()
        tree = TreeHTML(folders)

        if mode == 'nav':
            return tree.generate_folders_nav(current=current)

    @staticmethod
    def get_all(html = False):
        query = """
            SELECT
                node.folder_seo_content,
                node.folder_created,
                node.folder_parent,
                node.folder_name,
                node.folder_depth,
                node.folder_posts,
                node.folder_id,
                node.folder_left,
                node.folder_guid,
                node.folder_content,
                node.folder_slug,
                node.folder_right,
                node.folder_modified
            FROM
                {0}folder AS node,
                {0}folder AS parent
            WHERE
                node.folder_left BETWEEN parent.folder_left AND parent.folder_right
            GROUP BY
                node.folder_id
            ORDER BY
                node.folder_left, node.folder_id
        """.format(config.MYSQL_PREFIX)


        folders = Folder.query.sql(query).all(array=True)
        
        if not html:
            return folders
        
        if not folders:
            return ''

        tree = TreeHTML(folders)
        return tree.generate_folders_admin(False, 'sortable')

