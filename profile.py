from werkzeug.contrib.profiler import ProfilerMiddleware
from fypress import fypress

fypress.app.config['PROFILE'] = True
fypress.app.wsgi_app = ProfilerMiddleware(fypress.app.wsgi_app, restrictions=[30])
fypress.run()