"""
Django settings for leaderboard project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'leaderboard.sandstone',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework_gis',

    'leaderboard.contributors',
    'leaderboard.locations',
)

MIDDLEWARE_CLASSES = (
    'leaderboard.stats_middleware.StatsMiddleware',

    'csp.middleware.CSPMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'leaderboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'leaderboard.analytics_context.analytics_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'leaderboard.wsgi.application'

# Content Security Policy
CSP_REPORT_ONLY = True

CSP_DEFAULT_SRC = (
    "'none'",
)

CSP_SCRIPT_SRC = (
    "'self'",
    "mozorg.cdn.mozilla.net",
    "www.google-analytics.com",
    "www.mozilla.org",
)

CSP_STYLE_SRC = (
    "'unsafe-inline'",  # jQuery 1.7 uses inline styles
    "'self'",
    "www.mozilla.org",
)

CSP_IMG_SRC = (
    "'self'",
    "data:",
    "*.tiles.mapbox.com",
    "www.google-analytics.com",
    "www.mozilla.org",
)

CSP_CONNECT_SRC = (
    "'self'",  # API requests
)

CSP_OBJECT_SRC = (
    "'none'",
)

CSP_FRAME_ANCESTORS = (
    "'none'",
)

CSP_CHILD_SRC = (
    "'none'",
)

CSP_FONT_SRC = (
    "'self'",
    "www.mozilla.org",
)

CSP_BASE_URI = (
    "'none'"
)

CSP_REPORT_URI = (
    "/__cspreport__"
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'served/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.LimitOffsetPagination'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'leaderboard.parsers.GzipJSONParser',
    ),
    'PAGE_SIZE': 10,
}

# Geography Settings

# This project uses the Web Mercator projection system for specifying spatial coordinates
# http://spatialreference.org/ref/sr-org/7483/
WGS84_SRID = 4326
PROJECTION_SRID = 3857

# FXA Shared Settings
FXA_SCOPE = 'profile:uid profile:display_name profile:display_name:write profile:email'

# Google Analytics
GOOGLE_ANALYTICS_ID = 'Unknown'

# Git version info can be found in version.json
try:
    GIT_VERSION_INFO = json.loads(open(os.path.join(BASE_DIR, 'version.json')).read())
except (IOError, ValueError):
    # Unable to find version.json
    GIT_VERSION_INFO = ''

# Travis settings
if 'TRAVIS' in os.environ:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'travis'

    # Database configuration for travis tests
    # Should be overridden by a local settings file for actual deployments
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'leaderboard_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Firefox Accounts
    FXA_CLIENT_ID = 'travis'
    FXA_SECRET = 'travis'
    FXA_OAUTH_URI = 'travis'
    FXA_PROFILE_URI = 'travis'

# CircleCI
if 'CIRCLE' in os.environ:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'circle'

    # Database configuration for travis tests
    # Should be overridden by a local settings file for actual deployments
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'circle_test',
            'USER': 'ubuntu',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    # Firefox Accounts
    FXA_CLIENT_ID = 'circle'
    FXA_SECRET = 'circle'
    FXA_OAUTH_URI = 'circle'
    FXA_PROFILE_URI = 'circle'

# Docker build settings
if 'DOCKER_BUILD' in os.environ:
    SECRET_KEY = 'docker'

try:
    from settings_local import *
except:
    pass
