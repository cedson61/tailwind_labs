"""
Django settings for tailwind_labs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# PRODUCTION
import json
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

ADMINS = ('Howard Edson', 'howard.edson@gmail.com',)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "wi$w&#hqoc6og+n6dz6_x7*#z5!_luc6w&^m43nc()je6-im$%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.tailwindsolutions.com', ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'braces',
    'crispy_forms',
    'items',
    'csv_analyzer',
    'smart_sort',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tailwind_labs.urls'

WSGI_APPLICATION = 'tailwind_labs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'tailwind_labs_db',
          'USER': 'tailwind_user',
          'PASSWORD': 'several88',
          'HOST': 'web404.webfaction.com',
          'PORT': ''
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles' 

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/hedson/webapps/tailwind_labs_static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = 'tailwind_labs_login'
LOGOUT_URL = 'tailwind_labs_logout'
LOGIN_REDIRECT_URL = 'items:items_list'
