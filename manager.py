# -*- coding: UTF-8 -*-
from fypress import FyPress
from config import Config
import re

fypress = FyPress(Config, False)

from flask.ext.script import Manager
from fypress.user import User
from fypress.folder import Folder
from fypress.post import Post
from fypress.admin import Option
from fypress.local import _fypress_

app = fypress.app
db  = fypress.db

manager = Manager(app)


logo = """
░█▀▀▀ █  █ ░█▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ 
░█▀▀▀ █▄▄█ ░█▄▄█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ 
░█    ▄▄▄█ ░█    ▀ ▀▀ ▀▀▀ ▀▀▀ ▀▀▀                                                                                                                       
"""


@manager.command
def init_db():
    _fypress_.database.db.create_all()

    print '*** FyPress Database initialized.'
    return True

@manager.command
def init_fypress(login='', email='', passwd=''):
    if not passwd or not email or not login:
        print '*** /!\ Usage: python manager.py --login=name --email=your@email.com --passwd=yourpass'
        return False

    user = User.add(login, email, passwd)
    if user:
        user.status   = 4
        user.nicename = user.login
        user.save()
        print '*** Added user: '+str(user)
    else:
        print '*** /!\ Invalid user (Duplicate entry)'

    exist = Folder.get(Folder.id==1)
    if not exist:
        folder = Folder()
        folder.name     = 'Uncategorized'
        folder.id       = 1
        folder.guid     = ''
        
        folder.insert()       
        print '*** Added Folder: '+str(folder)

    options = [
        ['name', 'FyPress Site'],
        ['url',  Config.URL],
        ['slogan', 'Welcome to FyPress'],
        ['theme', 'Nyx']
    ]
    for option in options:
        opt = Option.update(option[0], option[1])
        print '*** Added Option: '+str(opt)

if __name__ == '__main__':
    print logo
    manager.run()