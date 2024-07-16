"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from pathlib import Path

from blacknoise import BlackNoise

from django.core.asgi import get_asgi_application

DEBUG = os.getenv('DEBUG') == 'true'
settings_module = 'dev' if DEBUG else 'prod'

os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE', 
  f'core.settings.{settings_module}'
)

BASE_DIR = Path(__file__).parent

application = BlackNoise(get_asgi_application())

application.add(BASE_DIR / "static", "/static")