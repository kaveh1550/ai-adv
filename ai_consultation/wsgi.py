"""
WSGI config for ai_consultation project.

It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_consultation'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_consultation.settings')

try:
    from django.core.wsgi import get_wsgi_application
except ImportError:
    raise ImportError("Couldn't import Django. Are you sure it's installed?")

application = get_wsgi_application()
