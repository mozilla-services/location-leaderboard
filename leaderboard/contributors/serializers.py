import datetime

from django.conf import settings
from django.contrib.gis.geos import Point
from rest_framework import serializers

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
        point = Point(
            data['tile_easting_m'],
            data['tile_northing_m'],
            srid=settings.PROJECTION_SRID,
        )
        point.transform(settings.WGS84_SRID)

        Contribution.objects.create(
            contributor=self.context['request'].user,
            date=datetime.datetime.fromtimestamp(data['time']).date(),
            observations=data['observations'],
            point=point,
        )

        return data
