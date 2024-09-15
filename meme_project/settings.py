import os
from pathlib import Path
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "SECRET_KEY"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'meme_app',
    'rest_framework',
    'storages',
]

# ... existing code ...
CSRF_TRUSTED_ORIGINS = [
    'https://11ec56d9-6098-4cdf-a77e-7bd53ae45d3f-00-1nku46o0soqjg.sisko.replit.dev:80',
    'http://11ec56d9-6098-4cdf-a77e-7bd53ae45d3f-00-1nku46o0soqjg.sisko.replit.dev:80',
    'https://11ec56d9-6098-4cdf-a77e-7bd53ae45d3f-00-1nku46o0soqjg.sisko.replit.dev:3000'
]
# ... existing code ...

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'meme_project.urls'

X_FRAME_OPTIONS = '*'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meme_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
database_url = os.environ.get("DATABASE_URL")

#DATABASES["default"] = dj_database_url.parse(database_url)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]



AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'eu-north-1'  # רק שם האזור

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



LANGUAGE_CODE = 'he'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'  # או 'profile' אם אתה רוצה להפנות לדף הפרופיל
LOGOUT_REDIRECT_URL = 'home'

AUTH_PROFILE_MODULE = 'meme_app.Profile'
