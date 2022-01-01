"""
ASGI config for newv project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

settings_exists = os.path.exists(
    os.path.join('.', 'fun', 'settings.py'))
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'fun.settings' if settings_exists else 'fun.settings_')

application = get_asgi_application()
