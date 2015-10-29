import datetime
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.models import (
    Contribution,
    ContributorRank,
)
from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.locations.tests.test_models import (
    CountryFactory,
    TileFactory,
)


class LeaderProfileTests(TestCase):

    def test_get_leader_profile_returns_ranks_and_observations(self):
        today = datetime.date.today()

        contributor = ContributorFactory()

        country1 = CountryFactory()
        country2 = CountryFactory()

        for country in (country1, country2):
            for i in range(3):
                Contribution.objects.create(
                    contributor=contributor,
                    date=today,
                    observations=1,
                    tile=TileFactory(country=country),
                )

        # Create the contributor ranks
        ContributorRank.compute_ranks()

        response = self.client.get(
            reverse(
                'leaders-profile',
                kwargs={'uid': contributor.uid},
            ),
        )

        self.assertEqual(response.status_code, 200)
        profile_data = json.loads(response.content)
        self.assertEqual(profile_data['uid'], contributor.uid)
        self.assertEqual(profile_data['name'], contributor.name)
        self.assertEqual(len(profile_data['ranks']), 3)
        self.assertIn({
            'country': None,
            'observations': 6,
            'rank': 1
        }, profile_data['ranks'])
        self.assertIn({
            'country': {
                'iso2': country1.iso2,
                'name': country1.name,
            },
            'observations': 3,
            'rank': 1
        }, profile_data['ranks'])
        self.assertIn({
            'country': {
                'iso2': country2.iso2,
                'name': country2.name,
            },
            'observations': 3,
            'rank': 1
        }, profile_data['ranks'])

    def test_bad_uid_raises_404(self):
        response = self.client.get(
            reverse(
                'leaders-profile',
                kwargs={'uid': 'asdf'},
            ),
        )

        self.assertEqual(response.status_code, 404)


class LeadersGlobalListTests(TestCase):

    def test_sums_for_each_contributor_and_orders_by_observations(self):
        today = datetime.date.today()

        country1 = CountryFactory()
        country2 = CountryFactory()

        contributor1 = ContributorFactory()

        for i in range(3):
            Contribution(
                contributor=contributor1,
                date=today,
                observations=1,
                tile=TileFactory(country=country1),
            ).save()

        contributor2 = ContributorFactory()

        for i in range(4):
            Contribution(
                contributor=contributor2,
                date=today,
                observations=1,
                tile=TileFactory(country=country2),
            ).save()

        # Create a contributor with no contributions
        # who should not appearin the leaderboard
        ContributorFactory()

        # Create the contributor ranks
        ContributorRank.compute_ranks()

        response = self.client.get(reverse('leaders-global-list'))
        self.assertEqual(response.status_code, 200)

        contributors_data = json.loads(response.content)
        self.assertEqual(contributors_data, {
            'count': 2,
            'previous': None,
            'results': [
                {
                    'uid': contributor2.uid,
                    'name': contributor2.name,
                    'observations': 4,
                    'rank': 1,
                }, {
                    'uid': contributor1.uid,
                    'name': contributor1.name,
                    'observations': 3,
                    'rank': 2,
                }
            ],
            'next': None,
        })

    def test_leaderboard_is_paginated(self):
        today = datetime.date.today()
        country = CountryFactory()
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

        for i in range(page_size + 1):
            contributor = ContributorFactory()
            Contribution(
                contributor=contributor,
                date=today,
                observations=1,
                tile=TileFactory(country=country),
            ).save()

        # Create the contributor ranks
        ContributorRank.compute_ranks()

        response = self.client.get(reverse('leaders-global-list'))
        self.assertEqual(response.status_code, 200)

        contributors_data = json.loads(response.content)
        self.assertEqual(len(contributors_data['results']), page_size)

        response = self.client.get(
            reverse('leaders-global-list'),
            {'offset': page_size},
        )
        self.assertEqual(response.status_code, 200)

        contributors_data = json.loads(response.content)
        self.assertEqual(len(contributors_data['results']), 1)


class LeaderCountryListViewTests(TestCase):

    def test_filters_by_country(self):
        today = datetime.date.today()

        contributor = ContributorFactory()

        country1 = CountryFactory()
        country2 = CountryFactory()

        contribution1 = Contribution(
            contributor=contributor,
            date=today,
            observations=1,
            tile=TileFactory(country=country1),
        )
        contribution1.save()

        contribution2 = Contribution(
            contributor=contributor,
            date=today,
            observations=1,
            tile=TileFactory(country=country1),
        )
        contribution2.save()

        contribution3 = Contribution(
            contributor=contributor,
            date=today,
            observations=1,
            tile=TileFactory(country=country2),
        )
        contribution3.save()

        # Create the contributor ranks
        ContributorRank.compute_ranks()

        response = self.client.get(
            reverse(
                'leaders-country-list',
                kwargs={'country_id': country1.iso2}
            )
        )
        self.assertEqual(response.status_code, 200)

        contributors_data = json.loads(response.content)
        self.assertEqual(contributors_data, {
            'count': 1,
            'previous': None,
            'results': [{
                'uid': contributor.uid,
                'name': contributor.name,
                'observations': 2,
                'rank': 1,
            }],
            'next': None,
        })

    def test_invalid_country_code_raises_404(self):
        response = self.client.get(
            reverse(
                'leaders-country-list',
                kwargs={'country_id': 'asdf'}
            )
        )
        self.assertEqual(response.status_code, 404)
