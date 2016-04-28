import datetime
import uuid

import factory
from django.conf import settings
from django.contrib.gis.geos import Point
from django.test import TestCase
from faker import Factory as FakerFactory

from leaderboard.contributors.models import (
    Contributor,
    ContributorRank,
    Contribution,
)
from leaderboard.locations.tests.test_models import CountryFactory


faker = FakerFactory.create()


class ContributorFactory(factory.DjangoModelFactory):
    uid = factory.LazyAttribute(lambda o: str(uuid.uuid4().hex))
    fxa_uid = factory.LazyAttribute(lambda o: str(uuid.uuid4().hex))
    name = factory.LazyAttribute(lambda o: faker.name())

    class Meta:
        model = Contributor


class ContributionFactory(factory.DjangoModelFactory):
    date = factory.LazyAttribute(lambda o: datetime.date.today())
    contributor = factory.SubFactory(ContributorFactory)
    point = factory.Sequence(
        lambda n: Point(n, n, srid=settings.WGS84_SRID))
    observations = 1

    class Meta:
        model = Contribution


class TestContributorRank(TestCase):

    def create_contribution(self, contributor, country):
        return Contribution.objects.create(
            contributor=contributor,
            date=datetime.date.today(),
            observations=1,
            point=country.geometry.point_on_surface,
        )

    def setUp(self):
        # There are two countries
        self.country1 = CountryFactory()
        self.country2 = CountryFactory()

        # And there are three contributors
        self.contributor1 = ContributorFactory()
        self.contributor2 = ContributorFactory()

        # Contributor3 makes no contributions
        self.contributor3 = ContributorFactory()

        # Contributor1 contributes 2 times to self.country1
        for i in range(2):
            self.create_contribution(self.contributor1, self.country1)

        # Contributor1 contributes 5 times to self.country2
        for i in range(5):
            self.create_contribution(self.contributor1, self.country2)

        # Contributor2 contributes 3 times to self.country1
        for i in range(3):
            self.create_contribution(self.contributor2, self.country1)

        # Contributor2 contributes 3 times to self.country2
        for i in range(3):
            self.create_contribution(self.contributor2, self.country2)

        # Compute the global and country ranks
        ContributorRank.compute_ranks()

    def test_compute_ranks_generates_one_rank_globally_and_per_country(self):
        # There are now 6 rank objects
        # Each contributor has:
        # 1 global
        # 1 self.country1
        # 1 self.country2
        self.assertEqual(ContributorRank.objects.count(), 6)

        for contributor in (self.contributor1, self.contributor2):
            for country in (None, self.country1, self.country2):
                self.assertTrue(
                    ContributorRank.objects.filter(
                        contributor=contributor, country=country).exists())

    def test_compute_ranks_sums_and_ranks_global_contributions(self):
        # Contributor1 is the global leader with 7 contributions
        contributor1_global_rank = (
            ContributorRank.objects.all_global().get(
                contributor=self.contributor1)
        )
        self.assertEqual(contributor1_global_rank.observations, 7)
        self.assertEqual(contributor1_global_rank.rank, 1)

        # Contributor2 is the global second with 6 contributions
        contributor2_global_rank = (
            ContributorRank.objects.all_global().get(
                contributor=self.contributor2)
        )
        self.assertEqual(contributor2_global_rank.observations, 6)
        self.assertEqual(contributor2_global_rank.rank, 2)

    def test_compute_ranks_sums_and_ranks_country_contributions(self):
        # Contributor2 is the self.country1 leader with 3 contributions
        contributor2_country1_rank = ContributorRank.objects.get(
            contributor=self.contributor2, country=self.country1)
        self.assertEqual(contributor2_country1_rank.observations, 3)
        self.assertEqual(contributor2_country1_rank.rank, 1)

        # Contributor1 is the self.country1 second with 2 contributions
        contributor1_country1_rank = ContributorRank.objects.get(
            contributor=self.contributor1, country=self.country1)
        self.assertEqual(contributor1_country1_rank.observations, 2)
        self.assertEqual(contributor1_country1_rank.rank, 2)

        # Contributor1 is the self.country2 leader with 5 contributions
        contributor1_country2_rank = ContributorRank.objects.get(
            contributor=self.contributor1, country=self.country2)
        self.assertEqual(contributor1_country2_rank.observations, 5)
        self.assertEqual(contributor1_country2_rank.rank, 1)

        # Contributor2 is the self.country2 second with 3 contributions
        contributor2_country2_rank = ContributorRank.objects.get(
            contributor=self.contributor2, country=self.country2)
        self.assertEqual(contributor2_country2_rank.observations, 3)
        self.assertEqual(contributor2_country2_rank.rank, 2)

    def test_contributor_ranks_are_ordered_by_decreasing_observations(self):
        ranks = ContributorRank.objects.all_global()

        self.assertEqual(
            [rank.contributor for rank in ranks],
            [self.contributor1, self.contributor2],
        )

    def test_compute_ranks_ignores_contributors_with_no_contributions(self):
        self.assertFalse(ContributorRank.objects.filter(
            contributor=self.contributor3).exists())

    def test_new_contributions_updates_existing_ranks(self):
        self.assertEqual(ContributorRank.objects.count(), 6)

        self.create_contribution(self.contributor1, self.country1)

        ContributorRank.compute_ranks()

        self.assertEqual(ContributorRank.objects.count(), 6)
        rank = ContributorRank.objects.get(
            contributor=self.contributor1, country=self.country1)

        self.assertEqual(rank.observations, 3)

    def test_compute_ranks_removes_observations_when_complete(self):
        self.assertEqual(Contribution.objects.count(), 0)

        for i in range(3):
            self.create_contribution(self.contributor1, self.country1)

        self.assertEqual(Contribution.objects.count(), 3)

        ContributorRank.compute_ranks()

        self.assertEqual(Contribution.objects.count(), 0)

    def test_contribution_set_frozen_during_rank_computation(self):
        contributor = ContributorFactory()
        country = CountryFactory()

        self.assertEqual(Contribution.objects.count(), 0)

        for i in range(3):
            self.create_contribution(contributor, country)

        self.assertEqual(Contribution.objects.count(), 3)

        contributions = list(Contribution.objects.all().select_related())
        self.assertEqual(Contribution.objects.count(), 3)

        for i in range(3):
            self.create_contribution(contributor, country)

        self.assertEqual(Contribution.objects.count(), 6)

        ContributorRank._compute_ranks(contributions)

        self.assertEqual(ContributorRank.objects.get(
            contributor=contributor, country=None).observations, 3)
        self.assertEqual(Contribution.objects.count(), 3)

    def test_compute_ranks_updates_existing_ranks(self):
        self.assertEqual(ContributorRank.objects.get(
            country=None, contributor=self.contributor1).rank, 1)
        self.assertEqual(ContributorRank.objects.get(
            country=None, contributor=self.contributor2).rank, 2)

        ContributionFactory(contributor=self.contributor2, observations=10)

        ContributorRank.compute_ranks()

        self.assertEqual(ContributorRank.objects.get(
            country=None, contributor=self.contributor1).rank, 2)
        self.assertEqual(ContributorRank.objects.get(
            country=None, contributor=self.contributor2).rank, 1)
