from rest_framework import serializers

from leaderboard.contributors.models import Contributor


class LeaderSerializer(serializers.ModelSerializer):
    """
    Serialize a contributor with their name and the
    number of observations they've made.
    """
    observations = serializers.IntegerField()

    class Meta:
        model = Contributor
        fields = ('name', 'observations')
