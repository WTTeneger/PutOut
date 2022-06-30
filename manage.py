#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from loguru import logger

logger.add('logs/info_{time}.log',
           format="{time} {level} {message}",
           level="INFO")  # , rotation="12:00")
logger.add('logs/debug_{time}.log',
           format="{time} {level} {message}",
           level="DEBUG")  # , rotation="12:00")



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lt.settings')
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
    # print('ss')
    main()
