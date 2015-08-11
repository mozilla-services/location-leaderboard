import datetime

from rest_framework import serializers

from leaderboard.contributors.models import Contributor, Contribution
from leaderboard.locations.models import Tile


class LeaderSerializer(serializers.ModelSerializer):
    """
    Serialize a contributor with their name and the
    number of observations they've made.
    """
    observations = serializers.IntegerField()

    class Meta:
        model = Contributor
        fields = ('name', 'observations')


class ContributionSerializer(serializers.Serializer):
    """
    A contribution submission from a contributor.  A contribution
    contains information about a tile and the number of observations
    made within taht tile.
    """
    time = serializers.FloatField()
    tile_northing_m = serializers.IntegerField()
    tile_easting_m = serializers.IntegerField()
    observations = serializers.IntegerField()

    def create(self, data):
        date = datetime.datetime.fromtimestamp(data['time']).date()

        tile, created = Tile.objects.get_or_create_nearest_tile(
            easting=data['tile_easting_m'], northing=data['tile_northing_m'])

        contribution, created = Contribution.objects.get_or_create(
            date=date,
            tile=tile,
            contributor=self.context['request'].user,
        )

        contribution.observations += data['observations']
        contribution.save()

        return data
