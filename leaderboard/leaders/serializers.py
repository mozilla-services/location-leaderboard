from rest_framework import serializers

from leaderboard.contributors.models import ContributorRank


class LeaderSerializer(serializers.ModelSerializer):
    """
    Serialize a contributor with their name and the
    number of observations they've made.
    """
    contributor = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    class Meta:
        model = ContributorRank
        fields = ('contributor', 'observations', 'rank')
