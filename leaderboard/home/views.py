from django.conf import settings
from django.db import connections, OperationalError
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView


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


class HeartbeatView(APIView):

    def get(self, request):
        response = 200

        try:
            # Test that we are able to connect to the
            # database
            connections['default'].cursor()
        except OperationalError:
            response = 400

        return Response(status=response)
