from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response


class LandingView(TemplateView):
    template_name = 'home/landing.html'


class VersionView(APIView):

    def get(self, request):
        return Response({
            'commit': settings.GIT_COMMIT,
            'source': settings.GIT_SOURCE,
            'tag': settings.GIT_TAG,
            'version': settings.GIT_VERSION,
        }, content_type='application/json')
