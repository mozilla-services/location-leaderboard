from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView, ListAPIView

from leaderboard.locations.models import Country
from leaderboard.contributors.models import Contributor, ContributorRank
from leaderboard.leaders.serializers import (
    LeaderProfileSerializer,
    LeaderListSerializer,
)


class LeaderProfileView(RetrieveAPIView):
    queryset = Contributor.objects.all()
    lookup_field = 'uid'
    serializer_class = LeaderProfileSerializer


class LeadersGlobalListView(ListAPIView):
    queryset = ContributorRank.objects.all_global()
    serializer_class = LeaderListSerializer


class LeadersCountryListView(LeadersGlobalListView):
    queryset = ContributorRank.objects.all()

    def get(self, *args, **kwargs):
        if not Country.objects.filter(iso2=self.kwargs['country_id']).exists():
            raise NotFound('Unknown country code.')

        return super(LeadersCountryListView, self).get(*args, **kwargs)

    def get_queryset(self):
        return super(
            LeadersCountryListView,
            self,
        ).get_queryset().filter(country__iso2=self.kwargs['country_id'])
