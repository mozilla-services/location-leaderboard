from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from leaderboard.locations.models import Country


class CountrySerializer(serializers.ModelSerializer):
    mpoly = GeometryField()

    class Meta:
        model = Country
        fields = ('id', 'name', 'mpoly')
