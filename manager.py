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
    try:
        con = db.connect().test()
    except:
        print '*** /!\ MySQL user or pass incorrect, please check config.py'
        return False
    
    statement = ""
    for line in open('./sql/all.sql'):
        if re.match(r'--', line):  
            continue
        if not re.search(r'[^-;]+;', line): 
            statement = statement + line
        else:  
            statement = statement + line
            try:
                statement = statement.replace('`fypress_', '`'+Config.MYSQL_PREFIX)
                con.cursor().execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

            statement = ""
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
        User.query.update(user)
        print '*** Added user: '+str(user)
    else:
        print '*** /!\ Invalid user (Duplicate entry)'

    exist = Folder.query.get(1)
    if not exist:
        folder = Folder()
        folder.name     = 'Uncategorized'
        folder.created  = 'NOW()'
        folder.modified = 'NOW()'
        folder.id       = 1
        folder.guid     = ''
        
        Folder.query.add(folder)
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