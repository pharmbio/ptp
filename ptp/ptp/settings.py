import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ptp_for_president_CC44aAFG'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
if os.environ.get('DEBUG', False) == 'True':
    DEBUG = True


ALLOWED_HOSTS = ['*', 'localhost']

CSRF_TRUSTED_ORIGINS=['https://ptp2-inference.serve.scilifelab.se']




# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ptp',
    'inference',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ptp.urls'

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

WSGI_APPLICATION = 'ptp.wsgi.application'

DATABASE_DIR = Path(os.environ.get('DATABASE_DIR', BASE_DIR))
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "staticsource",
    #'/var/www/static',
]


# Media files (Uploaded files, results)
MEDIA_URL = '/media/'

MEDIA_DIR = os.environ.get('MEDIA_DIR', BASE_DIR)
MEDIA_ROOT = os.path.join(MEDIA_DIR, 'media')

# Email settings (for sending job completion notifications)
if os.environ.get('EMAIL_HOST', False):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.example.com')
    EMAIL_PORT = os.environ.get('EMAIL_PORT',587)
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS',True)
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','your-email@example.com')

    # Not superfond of this..
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','your-email-password')
    # Perhaps?
    if os.environ.get("EMAIL_PASSWORD_FILE", False):
        filename = os.environ.get("EMAIL_PASSWORD_FILE", False)
        with open(filename) as f:
            EMAIL_HOST_PASSWORD = f.read().strip()

else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Use console backend for testing

# Celery configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TIMEZONE = 'Europe/Stockholm'

#CELERY_BROKER_URL = 'redis://redis:6379/0'
#CELERY_RESULT_BACKEND = 'django-db'  # Use Django database for Celery results
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_TIMEZONE = 'UTC'


# Use Django's static file handling system for serving uploaded files in development
# In production, it's better to use a cloud storage solution like AWS S3

# Set the SITE_URL for generating download links in emails

SITE_URL = os.environ.get('EMAIL_DOMAIN','https://ptp2-inference.serve.scilifelab.se')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG