from werkzeug.local import Local, LocalProxy

local     = Local()
_fypress_ = LocalProxy(local, 'fp')