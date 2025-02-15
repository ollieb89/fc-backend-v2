"""
WSGI config for fc-backend-v2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Check for the WEBSITE_HOSTNAME environment variable to see if we are running in Azure Ap Service
# If so, then load the settings from production.py
settings_module = 'fc-backend-v2.production' if 'WEBSITE_HOSTNAME' in os.environ else 'fc-backend-v2.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend_v2.settings')

application = get_wsgi_application()
