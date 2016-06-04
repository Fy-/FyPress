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

    def count_posts(self):
        query = """
            UPDATE
              fypress_folder
            SET
              fypress_folder.folder_posts =(
                  SELECT
                    COUNT(*)
                  FROM
                    fypress_post
                  WHERE
                    fypress_post.post_parent = 0 AND fypress_post.post_folder_id = fypress_folder.folder_id
            )
        """        
        Folder.query.sql(query).execute()

    @staticmethod
    def update_all(data):
        if data:
            exist = []
            for item in data:
                print item
                if item.has_key('id') and item['id'] != '1':
                    exist.append(int(item['id']))
                    folder = Folder.query.get(item['id'])
                    folder.depth    = item['depth']
                    folder.left     = item['left']
                    folder.right    = item['right']
                    folder.parent   = item['parent_id']

                    folder.modified = 'NOW()'
                    folder.update()

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
            Folder.link_posts()



    def update(self):
        Folder.query.update(self)

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
    def link_posts():
        from fypress.post import Post 
        posts =  Post.query.filter(status='draft').all(array=True)+Post.query.filter(status='published').all(array=True)+Post.query.filter(status='trash').all(array=True)
        for post in posts:
            post.guid = post.guid_generate()
            Post.query.update(post)

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

