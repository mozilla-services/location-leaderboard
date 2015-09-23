from rest_framework import serializers

from leaderboard.locations.models import Country


class CountrySerializer(serializers.ModelSerializer):
    observations = serializers.IntegerField()

    class Meta:
        model = Country
        fields = ('iso2', 'name', 'observations', 'leaders_url')
