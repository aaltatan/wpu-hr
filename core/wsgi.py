"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

BASE_DIR = Path().resolve()
load_dotenv(BASE_DIR / '.env')

DEBUG = os.getenv('DEBUG') == 'true'

settings_module = 'dev' if DEBUG else 'prod'

os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE', 
  f'core.settings.{settings_module}'
)

application = get_wsgi_application()
