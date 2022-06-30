"""
WSGI config for lt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib import admin
# from core.main.management.commands import potrans
# admin.site.add_action(potrans)  # в админке


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lt.settings')

application = get_wsgi_application()
