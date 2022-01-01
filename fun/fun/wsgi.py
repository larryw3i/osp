"""
WSGI config for fun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_exists = os.path.exists(
    os.path.join('.', 'fun', 'settings.py'))
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'fun.settings' if settings_exists else 'fun.settings_')

application = get_wsgi_application()
