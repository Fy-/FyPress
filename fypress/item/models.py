# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext as gettext
from fypress.utils import tree, OrderedDefaultDict
import fy_mysql, pprint


class TreeHTML(object):
    def __init__(self, items):
        self.html       = ''
        self.items      = items
        self.tritems    = []

        self.convert()

        self.json_rdy   = self.convert_to_json(self.tritems)

    def convert(self):
        for item in self.items:
            self.tritems.append((item.id, item, item.left, item.right, item.parent))

    def generate(self, items=False, cls=''):
        if items == False:
            items = self.json_rdy

        self.html += '<ol class="{}">'.format(cls)
        for item in items:
            root = 'panel-info'
            self.html += '<li id="folder_{}">'.format(item['data'].id)

            if item['data'].id == 1:
                root = 'panel-success root'

            self.html += """
                <div class="panel  {0}">
                    <div class="panel-heading">
                        {1}
                        <span title="Click to delete item." data-id="{2}" class="deleteMenu btn btn-warning btn-xs"><i class="fa fa-times-circle" aria-hidden="true"></i> Delete</span>
                        <a title="Click to edit item." data-id="{2}" class="btn btn-info btn-xs editMenu "><i class="fa fa-pencil" aria-hidden="true"></i> Edit</a>
                    </div>
                    <div class="panel-body">
                        {3}
                    </div>
                </div>
            """.format(root, item['data'].name, item['data'].id, item['data'].content)

            if item.has_key('children'):
                self.generate(item['children'])

            self.html += '</li>'
        self.html += '</ol>'

        return self.html 

    @staticmethod
    def convert_to_json(data):
        node_index = dict()
        parent_index = dict()
        for node in data:
            node_index[node[0]] = node
            parent_index.setdefault(node[4],[]).append(node)

        def process_node(index):
            result = { 'data' : node_index[index][1] }
            for node in parent_index.get(index,[]):
                result.setdefault('children',[]).append(process_node(node[0]))
            return result

        node = process_node(1)
        return [node]

class Folder(fy_mysql.Base):
    # /sql/folder.sql
    folder_id               = fy_mysql.Column(etype='int', primary_key=True)
    folder_parent           = fy_mysql.Column(etype='int')
    folder_left             = fy_mysql.Column(etype='int')
    folder_right            = fy_mysql.Column(etype='int')
    folder_depth            = fy_mysql.Column(etype='int')
    folder_slug             = fy_mysql.Column(etype='string', unique=True)
    folder_name             = fy_mysql.Column(etype='string', unique=True)
    folder_modified         = fy_mysql.Column(etype='datetime')
    folder_created          = fy_mysql.Column(etype='datetime')
    folder_content          = fy_mysql.Column(etype='string')
    folder_seo_content      = fy_mysql.Column(etype='string')

    @staticmethod
    def get_all():
        query = """
            SELECT
              node.folder_seo_content,
              node.folder_created,
              node.folder_modified,
              node.folder_parent,
              node.folder_name,
              node.folder_depth,
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
        tree = TreeHTML(folders)
        return tree.generate(False, 'sortable')

