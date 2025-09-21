#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
        import pathlib

        # 🔍 DEBUG вывод для CI
        print("=== DEBUG CI SETTINGS ===", file=sys.stderr)
        print("BASE_DIR =", settings.BASE_DIR, file=sys.stderr)
        dirs = settings.TEMPLATES[0].get("DIRS") or []
        print("TEMPLATES DIRS =", dirs, file=sys.stderr)

        for d in dirs:
            p = pathlib.Path(d)
            print("DIR:", p, "exists:", p.exists(), file=sys.stderr)
            users_dir = p / "users"
            print(" users dir:", users_dir, "exists:", users_dir.exists(), file=sys.stderr)
            if users_dir.exists():
                try:
                    for child in sorted(users_dir.iterdir()):
                        print("  -", child.name, file=sys.stderr)
                except Exception as e:
                    print("  (could not list users dir)", e, file=sys.stderr)

        exp = pathlib.Path(settings.BASE_DIR) / "task_manager" / "templates" / "users" / "user_form.html"
        print("EXPECTED:", exp, "exists:", exp.exists(), file=sys.stderr)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
