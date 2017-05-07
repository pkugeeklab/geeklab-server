import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)
sys.path.insert(0, path_of_current_dir)
worker_class = 'sync'
workers = multiprocessing.cpu_count() * 2 + 1
chdir = path_of_current_dir
worker_connections = 1000
timeout = 10
max_requests = 2000
graceful_timeout = 10
loglevel = 'info'
reload = True
debug = False
# daemon = True
os.makedirs('run', exist_ok=True)
os.makedirs('logs', exist_ok=True)

bind = '{}:{}'.format('0.0.0.0', 5000)
pidfile = '{}/run/{}.pid'.format(path_of_current_dir, _file_name)
errorlog = '{}/logs/{}_error.log'.format(path_of_current_dir, _file_name)
accesslog = '{}/logs/{}_access.log'.format(path_of_current_dir, _file_name)
