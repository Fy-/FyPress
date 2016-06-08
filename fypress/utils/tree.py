# -*- coding: UTF-8 -*-
from flask import url_for

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


    def generate_folders_nav(self, items=False, cls='nav', current=''):
        if items == False:
            try:
                items = self.json_rdy[0]['children']
            except:
                return ''
                
        for item in items:
            if '/'+item['data'].guid+'/' in current:
                active = 'class="active"'                
            else: 
                active = ''

            if item.has_key('children'):
                self.html += ("""
                    <li>
                        <a  href="/{1}/" {2}>
                            {0}
                        </a>
                        <ul class="menu vertical">

                """).format(item['data'].name, item['data'].guid, active)

                self.generate_folders_nav(item['children'], 'dropdown', current)

                self.html += ("""
                            </ul>
                    </li>
                """)
            else:
                self.html += ("""
                    <li>
                        <a {3} href="/{2}/">{1}</a>
                    </li>
                """).format(cls, item['data'].name, item['data'].guid, active)
    

        return self.html 

 

    def generate_folders_admin(self, items=False, cls=''):
        if items == False:
            items = self.json_rdy

        self.html += '<ol class="{}">'.format(cls)
        for item in items:
            self.html += '<li id="folder_{}">'.format(item['data'].id)

            if item['data'].id == 1:
                self.html += """
                    <div class="panel-success root">
                        <div class="panel-heading">
                            <i class="fa fa-folder-open-o fa-fw"></i> {0}
                            <div class="pull-right"><i class="fa fa-file-text-o fa-fw"></i> {2}</div>
                        </div>
                    </div>
                """.format(item['data'].name, item['data'].id, item['data'].posts)
            else:
                self.html += ("""
                    <div class="panel panel-info nav-drag">
                        <div class="panel-heading">
                            {0}
                            <a  href="javascript:void(0)" data-toggle="confirmation" data-target="{1}" data-placement="left" data-id="{1}" class="deleteMenu btn btn-warning btn-xs"><i class="fa fa-times-circle" aria-hidden="true"></i> Delete</a>
                            <a title="Click to edit item." data-id="{1}" href="{5}" class="btn btn-info btn-xs editMenu "><i class="fa fa-pencil" aria-hidden="true"></i> Edit</a>
                        </div>
                        <div class="panel-body">
                            <div class="table-responsive">
                                <table class="table ">
                                    <tbody>
                                    <tr>
                                        <td>#{1} {0} ({4})</td>
                                        <td>{2}</td>
                                        <td class="text-right"><i class="fa fa-file-text-o fa-fw"></i> {3}</td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                """).format(
                    item['data'].name, 
                    item['data'].id, 
                    item['data'].content, 
                    item['data'].posts, 
                    item['data'].slug, 
                    url_for('admin.folders', edit=item['data'].id)
                )

            if item.has_key('children'):
                self.generate_folders_admin(item['children'])

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