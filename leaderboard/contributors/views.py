from django.conf import settings
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from leaderboard.locations.models import Country
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


class LeadersView(ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = LeaderSerializer

    def filtered_queryset(self):
        return super(LeadersView, self).get_queryset()

    def get_queryset(self):
        return self.filtered_queryset().annotate_observations()


class LeadersCountryView(LeadersView):

    def get(self, *args, **kwargs):
        if not Country.objects.filter(iso2=self.kwargs['country_id']).exists():
            raise NotFound('Unknown country code.')

        return super(LeadersCountryView, self).get(*args, **kwargs)

    def filtered_queryset(self):
        return super(
            LeadersCountryView,
            self,
        ).filtered_queryset().filter_country(self.kwargs['country_id'])
