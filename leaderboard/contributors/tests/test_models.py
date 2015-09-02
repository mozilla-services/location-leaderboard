import datetime

import factory
from django.test import TestCase

from leaderboard.contributors.models import (
    Contributor,
    ContributorRank,
    Contribution,
)
from leaderboard.locations.tests.test_models import (
    CountryFactory,
    TileFactory,
)


class ContributorFactory(factory.DjangoModelFactory):
    access_token = factory.Sequence(lambda n: str(n))
    uid = factory.Sequence(lambda n: str(n))
    name = factory.Sequence(lambda n: 'Contributor {}'.format(n))
    email = factory.Sequence(
        lambda n: 'contributor{}@contribute.org'.format(n))

    class Meta:
        model = Contributor


class ContributionFactory(factory.DjangoModelFactory):
    date = factory.LazyAttribute(lambda o: datetime.date.today())
    contributor = factory.SubFactory(ContributorFactory)
    tile = factory.SubFactory(TileFactory)
    observations = 1

    class Meta:
        model = Contribution


class TestContributorQuerySet(TestCase):

    def test_filter_country(self):
        country1 = CountryFactory()
        country2 = CountryFactory()

        contributor1 = ContributorFactory()
        contributor2 = ContributorFactory()
        contributor3 = ContributorFactory()

        ContributionFactory(
            contributor=contributor1,
            tile=TileFactory(country=country1),
        )

        ContributionFactory(
            contributor=contributor2,
            tile=TileFactory(country=country2),
        )

        ContributionFactory(
            contributor=contributor3,
            tile=TileFactory(country=country1),
        )

        ContributionFactory(
            contributor=contributor3,
            tile=TileFactory(country=country2),
        )

        contributors = Contributor.objects.filter_country(country2.iso2)
        self.assertEqual(set(contributors), set([contributor2, contributor3]))

    def test_annotate_observations(self):
        country = CountryFactory()

        contributor1 = ContributorFactory()

        for i in range(10):
            ContributionFactory(
                contributor=contributor1,
                tile=TileFactory(country=country),
            )

        contributor2 = ContributorFactory()

        for i in range(20):
            ContributionFactory(
                contributor=contributor2,
                tile=TileFactory(country=country),
            )

        annotated_contributors = Contributor.objects.annotate_observations()
        contributor_observations = [
            (contributor, contributor.observations) for
            contributor in annotated_contributors
        ]
        expected_observations = [(contributor2, 20), (contributor1, 10)]
        self.assertEqual(contributor_observations, expected_observations)

    def test_observations_annotated_and_filtered_by_country(self):
        contributor = ContributorFactory()

        country1 = CountryFactory()
        country2 = CountryFactory()

        for country in (country1, country2):
            for i in range(10):
                ContributionFactory(
                    contributor=contributor,
                    tile=TileFactory(country=country),
                )

        annotated_contributor = (Contributor.objects
                                            .filter_country(country1.iso2)
                                            .annotate_observations()
                                            .get())

        self.assertEqual(annotated_contributor.observations, 10)

        annotated_contributor = (Contributor.objects
                                            .annotate_observations()
                                            .get())

        self.assertEqual(annotated_contributor.observations, 20)


class TestContributorRank(TestCase):

    def create_contribution(self, contributor, country):
        return Contribution.objects.create(
            contributor=contributor,
            date=datetime.date.today(),
            observations=1,
            tile=TileFactory(country=country)
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
