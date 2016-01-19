from django.conf import settings


def analytics_context(request):
    return {
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }
