# -*- coding: utf-8 -*-
import sys; reload(sys); sys.setdefaultencoding("utf-8")
from fypress import fypress

def main():
    fypress.run()
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit()