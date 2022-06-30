# -*- coding: utf-8 -*-
import os, sys


sys.path.insert(0, '/var/www/u1705556/data/www/luckytrade.online/LTSite')
sys.path.insert(1, '/var/www/u1705556/data/djangoenv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'LTSite.lt.server'

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lt.server')
application = get_wsgi_application()