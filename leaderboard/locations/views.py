from rest_framework.generics import ListAPIView

from leaderboard.locations.models import Country
from leaderboard.locations.serializers import CountrySerializer


class ListCountriesView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all().annotate_observations()
