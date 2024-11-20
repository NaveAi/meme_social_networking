import os
from django.core.wsgi import get_wsgi_application
from meme_app.backup import check_and_restore_db
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meme_project.settings')

# הפעלת פונקציית השחזור ב-thread נפרד
restore_thread = threading.Thread(target=check_and_restore_db)
restore_thread.start()

application = get_wsgi_application()