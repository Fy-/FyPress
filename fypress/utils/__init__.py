# -*- coding: UTF-8 -*-
from collections import OrderedDict, Callable, defaultdict

class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory

def tree(): return OrderedDefaultDict(tree)
