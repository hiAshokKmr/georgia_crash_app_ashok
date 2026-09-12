import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application

# Auto-migrate and ensure superuser on Vercel boot
if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)

        # Ensure superuser exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_user = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin123')
        admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin123@.com')
        admin_pass = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin123')

        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(username=admin_user, email=admin_email, password=admin_pass)
            print(f"Auto-created superuser: {admin_user}")
    except Exception as e:
        print(f"Vercel auto-bootstrap status: {e}")


