from rest_framework import serializers

from leaderboard.contributors.models import Contributor, ContributorRank


class ContributorRankSerializer(serializers.ModelSerializer):
    """
    Serialize a contributors rank and number of observations
    they've made in a given country.
    """
    GLOBAL_SLUG = 'Global'

    country = serializers.SlugRelatedField(
        slug_field='iso2', read_only=True)

    class Meta:
        model = ContributorRank
        fields = ('country', 'observations', 'rank')

    def to_representation(self, obj):
        data = super(ContributorRankSerializer, self).to_representation(obj)
        # When country is set to None it denotes a global rank
        if data['country'] is None:
            data['country'] = self.GLOBAL_SLUG
        return data


class LeaderProfileSerializer(serializers.ModelSerializer):
    """
    Serialize a contributor with their name and a
    break down of all the contributions they've made
    globally and in each country they've contributed
    to.
    """
    ranks = ContributorRankSerializer(many=True)

    class Meta:
        model = Contributor
        fields = ('uid', 'name', 'ranks')


class LeaderListSerializer(serializers.ModelSerializer):
    """
    Serialize a contributor with their name and the
    number of observations they've made.
    """
    uid = serializers.SlugRelatedField(
        source='contributor', slug_field='uid', read_only=True)
    name = serializers.SlugRelatedField(
        source='contributor', slug_field='name', read_only=True)

    class Meta:
        model = ContributorRank
        fields = ('uid', 'name', 'observations', 'rank')
