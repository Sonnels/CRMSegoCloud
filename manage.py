#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def create_superuser_if_needed():
    """Create superuser if running in Railway and doesn't exist"""
    if os.getenv('RAILWAY_ENVIRONMENT'):
        try:
            import django
            django.setup()
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
            email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@segocloud.com')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'AdminSegoCloud2024!')
            
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Admin',
                    last_name='SegoCloud',
                    role=User.Role.Admin,
                    is_verified=True
                )
                print(f"✅ Superuser created: {username} ({email})")
            else:
                print(f"ℹ️  Superuser already exists: {username}")
        except Exception as e:
            print(f"❌ Error creating superuser: {e}")


if __name__ == '__main__':
    main()
    # Create superuser after Django is ready (only in Railway)
    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
        create_superuser_if_needed()