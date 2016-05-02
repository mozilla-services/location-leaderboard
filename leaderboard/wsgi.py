"""
WSGI config for leaderboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import django.conf
import logging
import os

from django.core.wsgi import get_wsgi_application

log = logging.getLogger('django')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leaderboard.settings")

application = get_wsgi_application()


# Initialize NewRelic if we configured it
newrelic_ini = getattr(django.conf.settings, 'NEWRELIC_INI', None)

if newrelic_ini:
    import newrelic.agent
    try:
        newrelic.agent.initialize(newrelic_ini)
    except Exception:
        log.exception('Failed to load new relic config.')

    application = newrelic.agent.wsgi_application()(application)
