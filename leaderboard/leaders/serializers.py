from rest_framework import serializers

from leaderboard.contributors.models import ContributorRank


class LeaderSerializer(serializers.ModelSerializer):
    """
    Serialize a contributor with their name and the
    number of observations they've made.
    """
    name = serializers.SlugRelatedField(
        source='contributor', slug_field='name', read_only=True)

    class Meta:
        model = ContributorRank
        fields = ('name', 'observations', 'rank')
