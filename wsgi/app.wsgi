import sys
import site
import logging

site.addsitedir('/home/group01/POSIF/venv/lib/python3.9/site-packages')
sys.path.insert(0, '/home/group01/POSIF/venv/lib/python3.9/site-packages')
sys.path.insert(0, '/home/group01/POSIF')

log_handler = logging.FileHandler('/var/log/posif/server_access.log')
log_handler.setLevel(logging.INFO)

from main import app as application
application.logger.addHandler(log_handler)
application.logger.setLevel(logging.INFO)

