from fysql import Table
from fypress.local import _fypress_

class FyPressTables(Table):
    db = _fypress_.database.db