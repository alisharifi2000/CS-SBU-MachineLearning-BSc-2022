import os
import multiprocessing

import prometheus_client
from prometheus_client.multiprocess import MultiProcessCollector

proc_name = 'ML'
pidfile = '/tmp/ml.pid'

port = os.environ.get('GUNICORN_PORT', 8000)
bind = '0.0.0.0:{}'.format(port)

workers = os.environ.get('GUNICORN__WORKERS', multiprocessing.cpu_count() * 2)
threads = max(1, multiprocessing.cpu_count() // 2)
timeout = 300

max_requests = 100

# Max http request size in byte
limit_request_line = 4094

accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info').lower()

preload = True
