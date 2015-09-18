from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from leaderboard.locations.models import Country


class CountrySerializer(serializers.ModelSerializer):
    geometry = GeometryField()
    observations = serializers.IntegerField()

    class Meta:
        model = Country
        fields = ('iso2', 'name', 'geometry', 'observations')
