import os
import schedule
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
import threading




def backup_db_to_google_drive():
    print("מתחיל גיבוי למסמכי גוגל דרייב")
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = 'google_api.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': 'db_backup.sqlite3'}
    media = MediaFileUpload('db.sqlite3', mimetype='application/octet-stream')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def check_and_restore_db():
    print("בודק אם יש צורך לשחזר את בסיס הנתונים")
    if not os.path.exists('db.sqlite3'):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        SERVICE_ACCOUNT_FILE = 'google_api.json'

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        results = service.files().list(pageSize=10, fields="files(id, name)", q="name='db_backup.sqlite3'").execute()
        items = results.get('files', [])

        if items:
            file_id = items[0]['id']
            request = service.files().get_media(fileId=file_id)
            with open('db.sqlite3', 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()

def schedule_backup():
    schedule.every().day.at("00:00").do(backup_db_to_google_drive)  # תזמון הגיבוי

# הוספת קריאה לפונקציה schedule_backup בלולאת run_backup
def run_backup():
    schedule_backup()  # הוספת תזמון
    while True:
        print("בודק אם יש פעולות מתוזמנות לביצוע...")
        schedule.run_pending()
        time.sleep(1)

# יצירת thread חדש עבור הגיבוי
backup_thread = threading.Thread(target=run_backup)
backup_thread.start()

# כאן תוכל להפעיל את השרת שלך
# לדוגמה: app.run() אם אתה משתמש ב-Flask