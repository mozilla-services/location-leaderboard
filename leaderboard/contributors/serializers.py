import datetime

from rest_framework import serializers

from leaderboard.contributors.models import Contributor, Contribution
from leaderboard.locations.models import Tile


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

        # TODO: Actually pass the user in through fxa
        contributor, created = Contributor.objects.get_or_create(
            name='derp', email='derp@derp.com')

        contribution, created = Contribution.objects.get_or_create(
            date=date,
            tile=tile,
            contributor=contributor,
        )

        contribution.observations += data['observations']
        contribution.save()

        return data
