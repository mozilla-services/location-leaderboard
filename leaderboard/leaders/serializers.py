from rest_framework import serializers

from leaderboard.contributors.models import Contributor, ContributorRank
from leaderboard.locations.models import Country


class ContributorRankCountrySerializer(serializers.ModelSerializer):
    """
    Serialize a country for a given contributor rank.
    """

    class Meta:
        model = Country
        fields = ('name', 'iso2')


class ContributorRankSerializer(serializers.ModelSerializer):
    """
    Serialize a contributors rank and number of observations
    they've made in a given country.
    """
    GLOBAL_SLUG = 'Global'

    country = ContributorRankCountrySerializer()

    class Meta:
        model = ContributorRank
        fields = ('country', 'observations', 'rank')


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
