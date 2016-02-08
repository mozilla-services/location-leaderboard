import datetime

from django.conf import settings
from django.contrib.gis.geos import Point
from rest_framework import serializers

from leaderboard.locations.models import Country
from leaderboard.contributors.models import Contribution


class ContributionSerializer(serializers.Serializer):
    """
    A contribution submission from a contributor.  A contribution
    contains information about a tile and the number of observations
    made within taht tile.
    """
    time = serializers.FloatField()
    tile_northing_m = serializers.FloatField()
    tile_easting_m = serializers.FloatField()
    observations = serializers.IntegerField()

    def create(self, data):
        date = datetime.datetime.fromtimestamp(data['time']).date()

        country = Country.objects.nearest_to_point(Point(
            data['tile_easting_m'],
            data['tile_northing_m'],
            srid=settings.PROJECTION_SRID,
        ))

        Contribution.objects.create(
            date=date,
            country=country,
            contributor=self.context['request'].user,
            observations=data['observations'],
        )

        return data
