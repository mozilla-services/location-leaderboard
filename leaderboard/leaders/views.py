from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView

from leaderboard.locations.models import Country
from leaderboard.contributors.models import ContributorCountryRank
from leaderboard.leaders.serializers import (
    LeaderSerializer,
)


class LeadersGlobalListView(ListAPIView):
    queryset = ContributorCountryRank.objects.all_global()
    serializer_class = LeaderSerializer


class LeadersCountryListView(LeadersGlobalListView):
    queryset = ContributorCountryRank.objects.all()

    def get(self, *args, **kwargs):
        if not Country.objects.filter(iso2=self.kwargs['country_id']).exists():
            raise NotFound('Unknown country code.')

        return super(LeadersCountryListView, self).get(*args, **kwargs)

    def get_queryset(self):
        return super(
            LeadersCountryListView,
            self,
        ).get_queryset().filter(country__iso2=self.kwargs['country_id'])
