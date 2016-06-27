import os


def getCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "unix:/tmp/gunicorn_fypress.sock"
workers = getCPUs()
backlog = 2048
worker_class = "gevent"
debug = True
daemon = False
pidfile = "/tmp/gunicorn-fypress.pid"
