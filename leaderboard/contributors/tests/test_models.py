import datetime

import factory
from django.test import TestCase

from leaderboard.contributors.models import Contributor, Contribution
from leaderboard.locations.tests.test_models import (
    CountryFactory,
    TileFactory,
)


class ContributorFactory(factory.DjangoModelFactory):
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
