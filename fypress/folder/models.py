# -*- coding: UTF-8 -*-
from fypress.utils import slugify, url_unique, TreeHTML
from fypress.models import FyPressTables
from fysql import CharColumn, DateTimeColumn, IntegerColumn, TextColumn
from fypress import FyPress

import datetime

fypress = FyPress()


def slug_setter(value):
    return slugify(value)


class Folder(FyPressTables):
    parent = IntegerColumn(index=True)
    left = IntegerColumn(index=True)
    right = IntegerColumn(index=True)
    depth = IntegerColumn(index=True)
    guid = CharColumn(index=True, max_length=255)
    slug = CharColumn(index=True, max_length=255, setter=slug_setter)
    posts = IntegerColumn()
    name = CharColumn(index=True, max_length=150)
    modified = DateTimeColumn(default=datetime.datetime.now)
    created = DateTimeColumn(default=datetime.datetime.now)
    content = TextColumn()
    seo_content = TextColumn()

    def count_posts(self):
        query = """
            UPDATE
              folder
            SET
              folder.posts =(
                  SELECT
                    COUNT(*)
                  FROM
                    post
                  WHERE
                    post.parent = 0 AND post.id = folder.id
            )
        """
        fypress.database.db.raw(query)

    @staticmethod
    def update_all(data):
        if data:
            exist = []
            for item in data:
                if item.has_key('id') and item['id'] != '1':
                    exist.append(int(item['id']))
                    folder = Folder.get(Folder.id == item['id'])
                    folder.depth = item['depth']
                    folder.left = item['left']
                    folder.right = item['right']
                    folder.parent = item['parent_id']

                    folder.modified = datetime.datetime.now()
                    folder.save()

            all_folders = []
            folders = Folder.all()
            for folder in folders:
                all_folders.append(int(folder.id))

            diff = [item for item in all_folders if item not in exist]
            for item in diff:
                if item != 1:
                    from fypress.post import Post
                    posts = Post.filter(Post.id_folder == item).all()
                    for post in posts:
                        post.id_folder = 1
                        post.save()
                    Folder.get(Folder.id == item).remove()

            for folder in folders:
                folder.count_posts()

            Folder.build_guid()
            from fypress.post import Post

            Post.link_posts()

    @staticmethod
    def update_guid(folder):
        query = """
          SELECT
            GROUP_CONCAT(parent.slug SEPARATOR '/') AS path
          FROM
            folder,
            folder AS parent
          WHERE
            folder.`left` BETWEEN parent.`left` AND parent.`right` AND folder.id={0} AND folder.id!=1
          ORDER BY
            parent.`left`""".format(folder.id)

        folder.guid = url_unique(fypress.database.db.raw(query).fetchone()[0], Folder, folder.id)
        folder.save()

    @staticmethod
    def build_guid():
        folders = Folder.all()
        for folder in folders:
            if folder.id != 1:
                Folder.update_guid(folder)

    @staticmethod
    def add(form):
        query = """SELECT MAX(`left`) as l, MAX(`right`) as r FROM folder"""
        rv = fypress.database.db.raw(query).fetchall()[0]

        if rv[0] == 0 and rv[1] == 0:
            r = 1
            l = 2
        else:
            r = rv[0]
            l = rv[1]

        folder = Folder.create()
        form.populate_obj(folder)
        folder.parent = 1
        folder.left = r + 1
        folder.right = l + 1
        folder.save()

        Folder.build_guid()

    @staticmethod
    def get_path(folder):
        return Folder.select(
            add_from='folder AS parent'
        ).where(
            'folder.`left` BETWEEN parent.`left` AND parent.`right` AND folder.id={0} AND folder.id!=1'.format(folder.id)
        ).order_by(
            'parent.`left`'
        ).all()

    @staticmethod
    def get_as_tree(mode='nav', current=''):
        folders = Folder.select(
            add_from='folder AS parent'
        ).where(
            'folder.`left` BETWEEN parent.`left` AND parent.`right`'
        ).group_by(
            'folder.id'
        ).order_by(
            'folder.`left`, folder.id'
        ).all()

        tree = TreeHTML(folders)

        if mode == 'nav':
            return tree.generate_folders_nav(current=current)

    @staticmethod
    def get_all(html=False):
        folders = Folder.select(
            add_from='folder AS parent'
        ).where(
            'folder.left BETWEEN parent.left AND parent.right'
        ).group_by(
            'folder.id'
        ).order_by(
            'folder.left, folder.id'
        ).all()

        if not html:
            return folders

        if not folders:
            return ''

        tree = TreeHTML(folders)
        return tree.generate_folders_admin(False, 'sortable')
