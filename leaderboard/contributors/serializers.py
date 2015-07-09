from rest_framework import serializers

from leaderboard.contributors.models import Contributor, Contribution
from leaderboard.locations.models import Tile


class ContributionSerializer(serializers.Serializer):
    """
    A contribution submission from a contributor.  A contribution
    contains information about a tile and the number of observations
    made within taht tile.
    """
    tile_north = serializers.IntegerField()
    tile_east = serializers.IntegerField()
    observations = serializers.IntegerField()

    def create(self, data):
        tile, created = Tile.objects.get_or_create_nearest_tile(
            east=data['tile_east'], north=data['tile_north'])

        # TODO: Actually pass the user in through fxa
        contributor, created = Contributor.objects.get_or_create(
            name='derp', email='derp@derp.com')
        Contribution.objects.create(
            tile=tile,
            contributor=contributor,
            observations=data['observations'],
        )
        return data
