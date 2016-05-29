# -*- coding: UTF-8 -*-
import fy_mysql

class Option(fy_mysql.Base):
    # /sql/option.sql
    option_id               = fy_mysql.Column(etype='int', primary_key=True)
    option_name             = fy_mysql.Column(etype='string', unique=True)
    option_value            = fy_mysql.Column(etype='string')
    option_load             = fy_mysql.Column(etype='int')

    def __init__(self):
        pass
    
    @staticmethod
    def auto_load():
        final   = {}
        options = Option.query.filter(load=1).all()
        for option in options:
            final[option.name] = option.value 

        return final