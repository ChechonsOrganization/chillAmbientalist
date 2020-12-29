"""
WSGI config for chillAmbientalist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Cambiar en os.environ 'chillAmbientalist.settings' a 'chillAmbientalist.settings.dev'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chillAmbientalist.settings.dev')

application = get_wsgi_application()
