"""
WSGI config for djtest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os, sys

proj = os.path.dirname(__file__)
projs = os.path.dirname(proj)
if projs not in sys.path:
    sys.path.append(proj)
    sys.path.append(projs)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
