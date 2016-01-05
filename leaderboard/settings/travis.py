from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
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
