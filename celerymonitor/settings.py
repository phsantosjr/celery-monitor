import os
# import djcelery
from django.urls import reverse_lazy
from pathlib import Path
from decouple import config, Csv
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Application definition

INSTALLED_APPS = [
    "channels",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
EXTRA_APPS = [
    # 'djcelery',
    'bootstrap3',
    'rest_framework',
    'rest_framework.authtoken',
]
PROJECT_APPS = [
    'django_admin',
    'celerymonitor',
    'monitor',
]
INSTALLED_APPS += EXTRA_APPS
INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = 'celerymonitor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'celerymonitor.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATE_INPUT_FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y"]


# AWS
AWS_ACCESS_KEY_ID = config("DO_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("DO_SECRET_ACCESS_KEY", default="")

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )

AWS_STORAGE_BUCKET_NAME = 'lojaconectada-celery-monitor'

DEFAULT_FILE_STORAGE = config(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    AWS_LOCATION = 'static'
    AWS_STATIC_LOCATION = 'static'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{AWS_STATIC_LOCATION}/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "celerymonitor.storage.MediaStorage"
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86200',
    }

MEDIA_AWS_BUCKET = AWS_STORAGE_BUCKET_NAME

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'monitor', 'locale'),
]
"""
djano celery to accomplish some async job configuration.
"""
# djcelery.setup_loader()

REDIS_ENDPOINT = f'redis://:{config("REDIS_PASSWORD")}@{config("BROKER_URL")}'
BROKER_URL = REDIS_ENDPOINT
broker_url = BROKER_URL
CELERY_RESULT_BACKEND = REDIS_ENDPOINT
CELERY_ACCEPT_CONTENT = ['application/json']  
CELERY_TASK_SERIALIZER = 'json'  
CELERY_RESULT_SERIALIZER = 'json'  
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_TASK_RESULT_EXPIRES = 1200
CELERY_APPLICATION_PATH = 'celerymonitor.celeryapp.app'
CELERY_ENABLE_UTC = True
# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
'''
Task hard time limit in seconds.
The worker processing the task will be killed and replaced with a new one when this is exceeded.
'''
CELERYD_TASK_TIME_LIMIT = 86400
# CELERYD_TASK_TIME_LIMIT = 10
CELERYD_CONCURRENCY=30

# CELERYBEAT_LOG_LEVEL=INFO

# CELERYD_LOG_LEVEL=INFO
'''
Task soft time limit in seconds.
The SoftTimeLimitExceeded exception will be raised when this is exceeded. The task can catch this to e.g.
clean up before the hard time limit comes.
'''
CELERYD_TASK_SOFT_TIME_LIMIT = 80000

CELERY_IMPORTS = ("celerymonitor.tasks",)
CELERY_REDIS_MAX_CONNECTIONS = 0

# send celerymon
CELERY_SEND_EVENTS = True
CELERYD_POOL_RESTARTS = True
CELERYD_MAX_TASKS_PER_CHILD = 50

#TEMPLATE_DEBUG = True
#from celery.schedules import crontab

#CELERYBEAT_SCHEDULE = {
    ## Executes every Monday morning at 7:30 A.M
    #'add-every-monday-morning': {
        #'task': 'celerymonitor.celeryapp.debug_task',
        #'schedule': crontab(hour=7, minute=30, day_of_week=1),
        #'args': (16, 16),
    #},
#}


ASGI_APPLICATION = "celerymonitor.asgi.application"

CHANNEL_LAYERS = {
    "default": {
       "BACKEND": "channels_redis.core.RedisChannelLayer",  # use redis backend
       "CONFIG": {
           "hosts": [REDIS_ENDPOINT],  # set redis address
           },
       "ROUTING": "celerymonitor.routing.channel_routing",  # load routing from our routing.py file
       },
}

LANGUAGES = [
    ('zh-hans', _('Simple Chinese')),
    ('en', _('English')),
]

# Restful api setting
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }