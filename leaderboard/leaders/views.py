from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView

from leaderboard.locations.models import Country
from leaderboard.contributors.models import Contributor
from leaderboard.leaders.serializers import (
    LeaderSerializer,
)


class LeadersGlobalListView(ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = LeaderSerializer

    def filtered_queryset(self):
        return super(LeadersGlobalListView, self).get_queryset()

    def get_queryset(self):
        return self.filtered_queryset().annotate_observations()


class LeadersCountryListView(LeadersGlobalListView):

    def get(self, *args, **kwargs):
        if not Country.objects.filter(iso2=self.kwargs['country_id']).exists():
            raise NotFound('Unknown country code.')

        return super(LeadersCountryListView, self).get(*args, **kwargs)

    def filtered_queryset(self):
        return super(
            LeadersCountryListView,
            self,
        ).filtered_queryset().filter_country(self.kwargs['country_id'])
