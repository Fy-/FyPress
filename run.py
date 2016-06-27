# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from fypress import FyPress
from config import Config


def main():
    fypress = FyPress(Config)
    fypress.run()
    return 0

if __name__ == '__main__':
    main()
    sys.exit()
