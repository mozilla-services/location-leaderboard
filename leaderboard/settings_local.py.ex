##############
# PRODUCTION #
##############

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    # All production DNS names must appear in here
    # example:
    # 'leaderboard.mozilla.org',
]

###############
# DEVELOPMENT #
###############
# Enable to set `debug` context variable within templates
# This is for DEVELOPMENT environments ONLY
#class IPList(object):
#
#    def __contains__(self, *args, **kwargs):
#        return True
#
#INTERNAL_IPS = IPList()


##########
# SHARED #
##########

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'TODO',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'TODO',
        'PASSWORD': 'TODO',
        'HOST': 'TODO',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': 'TODO',                      # Set to empty string for default.
    }
}

# Firefox Accounts
FXA_CLIENT_ID = 'TODO'
FXA_SECRET = 'TODO'
FXA_OAUTH_URI = 'https://oauth-stable.dev.lcip.org/v1/'
FXA_PROFILE_URI = 'https://stable.dev.lcip.org/profile/v1/'
