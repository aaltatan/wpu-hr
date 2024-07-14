#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


def main(settings_module: str):
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{settings_module}')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    
    BASE_DIR = Path().resolve()
    load_dotenv(BASE_DIR / '.env')
    
    DEBUG = os.getenv('DEBUG') == 'true'
    
    settings_module = 'dev' if DEBUG else 'prod'
    
    main(settings_module)
