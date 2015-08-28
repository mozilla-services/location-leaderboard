import datetime
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.models import Contribution
from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.locations.tests.test_models import (
    CountryFactory,
    TileFactory,
)


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

        response = self.client.get(reverse('leaders-global-list'))
        self.assertEqual(response.status_code, 200)

        contributors_data = json.loads(response.content)
        self.assertEqual(contributors_data, {
            'count': 2,
            'previous': None,
            'results': [
                {
                    'name': contributor2.name,
                    'observations': 4,
                }, {
                    'name': contributor1.name,
                    'observations': 3,
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

        response = self.client.get(reverse('leaders-global-list'))
        self.assertEqual(response.status_code, 200)

        contributors_data = json.loads(response.content)
        self.assertEqual(len(contributors_data['results']), page_size)

        response = self.client.get(reverse('leaders-global-list'), {'page': 2})
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
                'name': contributor.name,
                'observations': 2,
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
