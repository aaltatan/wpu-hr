from .base import *
from getpass import getpass


DEBUG = False

ALLOWED_HOSTS = ['*']


if os.getenv('DB') == 'sqlite':
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'app.db',
      }
  }
else:
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': getpass('DB password: '),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
  }

STATIC_ROOT = BASE_DIR / 'static'
