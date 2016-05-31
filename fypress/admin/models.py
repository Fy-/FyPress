# -*- coding: UTF-8 -*-
from fypress.utils import mysql

class Option(mysql.Base):
    # /sql/option.sql
    option_id               = mysql.Column(etype='int', primary_key=True)
    option_name             = mysql.Column(etype='string', unique=True)
    option_value            = mysql.Column(etype='string')
    option_load             = mysql.Column(etype='int')

    def __init__(self):
        pass
    
    @staticmethod
    def auto_load():
        final   = {}
        options = Option.query.filter(load=1).all()
        for option in options:
            final[option.name] = option.value 

        return final