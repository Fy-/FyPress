# -*- coding: UTF-8 -*-
from fypress.models import FyPressTables
from fysql import CharColumn, TextColumn, BooleanColumn

class Option(FyPressTables):
    name  = CharColumn(pkey=True, unique=True, index=True, max_length=75)
    value = TextColumn()
    load  = BooleanColumn(index=True)

    @staticmethod
    def auto_load():
        final   = {}
        options = Option.filter(Option.load==1).all()
        for option in options:
            final[option.name] = option.value 

        return final

    @staticmethod
    def update(name, value, auto_load=1):
        option = Option.get(Option.name==name)
        if option:
            option.value = value
            option.save()
        else:
            option = Option.create(name=name, value=value, load=auto_load)

        return option

    @staticmethod
    def get_value(name):
        option = Option.get(Option.name==name)
        if option:
            return option.value
        return False

    @staticmethod
    def get_settings(option_type='general'):
        settings = {
            'general': ['name', 'url', 'slogan', 'footer'],
            'social' : ['analytics', 'twitter', 'facebook', 'github'],
            'design' : ['logo', 'ico', 'css']
        }

        class Result(object):
            """ wtform """
            def set(self, name, value):
                setattr(self, name, value)

        result  = Result()
        options = Option.filter(Option.name << settings[option_type]).all()
        for option in options:
            result.set(option.name, option.value)

        return result