from fysql import Table
from fypress import FyPress

fypress = FyPress()


class FyPressTables(Table):
    db = fypress.database.db
