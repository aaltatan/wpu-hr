from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '172.25.0.23'
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INSTALLED_APPS += ['debug_toolbar']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'app.db',
    }
}

STATICFILES_DIRS = [
  BASE_DIR / "static"
]

INTERNAL_IPS = [
    "127.0.0.1",
]