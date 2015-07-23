from django.db.models import Sum
from django.conf import settings
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from leaderboard.contributors.models import Contributor
from leaderboard.contributors.serializers import (
    LeaderSerializer,
    ContributionSerializer,
)


class ContributionsConfigView(APIView):

    def get(self, request):
        config_data = {
            'tile_size': settings.CONTRIBUTION_TILE_SIZE,
            'record_duration': settings.CONTRIBUTION_RECORD_DURATION,
        }
        return Response(config_data, content_type='application/json')


class CreateContributionsView(CreateAPIView):
    """
    Create a contribution from user submitted data.
    """
    serializer_class = ContributionSerializer

    def get_serializer(self, data=None, *args, **kwargs):
        if data:
            data = data.get('items', [])
        return super(CreateContributionsView, self).get_serializer(
            data=data, many=True, *args, **kwargs)


class LeadersCountryView(ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = LeaderSerializer

    def get_queryset(self):
        return super(
            LeadersCountryView,
            self,
        ).get_queryset().filter(
            contribution__tile__country_id=self.kwargs['country_id']
        ).annotate(
            observations=Sum('contribution__observations')
        ).order_by('-observations')
