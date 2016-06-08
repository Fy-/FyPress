# -*- coding: UTF-8 -*-
from fypress.utils import mysql

class Option(mysql.Base):
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

    @staticmethod
    def update(name, value, auto_load=1):
        option = Option.query.filter(name=name).one()
        if option:
            option.value = value
            Option.query.update(option)
        else:
            option = Option()
            option.name      = name
            option.value     = value 
            option.auto_load = auto_load
            Option.query.add(option)

        return option

    @staticmethod
    def get(name):
        option = Option.query.filter(name=name).one()
        return option.value

    @staticmethod
    def get_settings(type='general'):
        settings = {
            'general': ['name', 'url', 'slogan'],
            'social' : ['twitter', 'facebook', 'github'],
            'design' : ['logo', 'ico']
        }

        class Result(object):
            def set(self, name, value):
                setattr(self, name, value)


        result  = Result()
        options = Option.query.where('_table_.option_name IN ("'+'","'.join(settings[type])+'")').all()
        for option in options:
            result.set(option.name, option.value)

        return result