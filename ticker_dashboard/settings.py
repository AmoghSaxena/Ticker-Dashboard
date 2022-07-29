"""
Django settings for ticker_dashboard project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'. 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d4&p=e9c^vi$l@pm!&iebq@iqxffhxbq!423e9&d04&ec8$&n_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = ['https://ticker.dns.army']

CORS_REPLACE_HTTPS_REFERER = True

CSRF_COOKIE_DOMAIN = 'ticker.dns.army'

# CORS_ORIGIN_WHITELIST = (
#     'https://front.bluemix.net/',
#     'front.bluemix.net',
#     'bluemix.net',
# )

# Application definition

INSTALLED_APPS = [
    'admin_volt.apps.AdminVoltConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'directory',
    'ticker_management',
    'django_celery_results',
    'django_celery_beat'
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

ROOT_URLCONF = 'ticker_dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'template'],
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

WSGI_APPLICATION = 'ticker_dashboard.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.axolites.com'
EMAIL_HOST_USER = 'ticker@axolites.com'
EMAIL_HOST_PASSWORD = '92b9a3b730#123'
DEFAULT_FROM_EMAIL = 'ticker@axolites.com'
SERVER_EMAIL = 'ticker@axolites.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Ticker',
        'USER': 'Ticker',
        'PASSWORD': '92b9a3b730',
        'HOST': 'mariadb',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
LOGOUT_REDIRECT_URL = "/"
SESSION_EXPIRE_SECONDS = 12

# Static files (CSS, JavaScript, Images)

if DEBUG:
    STATICFILES_DIRS = [
    BASE_DIR,"static"
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Media 
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



#CELERY SETTINGS

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_ACCEPT_CONTEXT = ['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'
CELERY_TIMEZONE='Asia/Kolkata'

DJANGO_CELERY_BEAT_TZ_AWARE = False

CELERY_RESULT_BACKEND = 'django-db'

#CELERY BEAT SETTINGS

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

#127.0.0.1:6379


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
         'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.IsAuthenticated'
        #'knox.auth.TokenAuthentication',
    ]
}

# DIRECTORY_DIRECTORY = '/home/guest/Desktop/Ticker-Dashboard/media'

LOGGING = {
    'version': 1,
    'loggers':{
        'dashboardLogs':{
            'handlers':['infoLogs','warningLogs','errorLogs','criticalLogs'],
            'level':DEBUG
        }
    },
    'handlers':{
        'infoLogs':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'filename':BASE_DIR+'/logs/info.log',
            'formatter':'simple',
        },
        'warningLogs':{
            'level':'WARNING',
            'class':'logging.FileHandler',
            'filename':BASE_DIR+'/logs/warning.log',
            'formatter':'simple',
        },
        'errorLogs':{
            'level':'ERROR',
            'class':'logging.FileHandler',
            'filename':BASE_DIR+'/logs/error.log',
            'formatter':'simple',
        },
        'criticalLogs':{
            'level':'CRITICAL',
            'class':'logging.FileHandler',
            'filename':BASE_DIR+'/logs/critical.log',
            'formatter':'simple',
        }
    },
    'formatters':{
        'simple':{
            'format':'{levelname} {asctime} :  {module} {process:d} {message} from function {funcName} in line no. {lineno}',
            'style':'{',
        }
    }
}