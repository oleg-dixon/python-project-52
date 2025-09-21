#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from django.conf import settings
# import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
        import sys

        # 🔍 DEBUG вывод для CI
        print("=== DEBUG CI SETTINGS ===", file=sys.stderr)
        print("BASE_DIR =", settings.BASE_DIR, file=sys.stderr)
        print("TEMPLATES DIRS =", settings.TEMPLATES[0].get("DIRS"), file=sys.stderr)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
