# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from fypress import FyPress
from config import ConfigProd

fypress = FyPress(ConfigProd)
fypress_app = fypress.app
