import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meme_project.settings')
application = get_wsgi_application()

if os.getenv('MIGRATE_ON_START', 'false').lower() == 'true':
    call_command('migrate')
