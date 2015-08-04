import datetime
import json
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.models import Contribution
from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.locations.models import Tile
from leaderboard.locations.tests.test_models import (
    CountryFactory,
    CountryTestMixin,
    TileFactory,
)
from leaderboard.utils.compression import gzip_compress


class ContributionConfigTests(TestCase):

    def test_get_contribution_config(self):
        response = self.client.get(reverse('contributions-config'))

        self.assertEqual(response.status_code, 200)

        config_data = json.loads(response.content)

        self.assertEqual(config_data, {
            'tile_size': settings.CONTRIBUTION_TILE_SIZE,
            'record_duration': settings.CONTRIBUTION_RECORD_DURATION,
        })


class SubmitContributionTests(CountryTestMixin, TestCase):

    def test_submit_multiple_observations(self):
        now = time.time()
        one_day = 24 * 60 * 60

        observation_data = {
            'items': [
                # A contribution for tile1 at time1
                {
                    'time': now,
                    'tile_easting_m': -8872100,
                    'tile_northing_m': 5435700,
                    'observations': 100,
                },
                # A contribution for tile1 at time 1
                {
                    'time': now,
                    'tile_easting_m': -8872100,
                    'tile_northing_m': 5435700,
                    'observations': 100,
                },
                # A contribution for tile2 at time1
                {
                    'time': now,
                    'tile_easting_m': -8892100,
                    'tile_northing_m': 5435700,
                    'observations': 100,
                },
                # A contribution for tile2 at time2
                {
                    'time': now + one_day,
                    'tile_easting_m': -8892100,
                    'tile_northing_m': 5435700,
                    'observations': 100,
                },
            ],
        }

        payload = json.dumps(observation_data)

        response = self.client.post(
            reverse('contributions-create'),
            payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Tile.objects.all().count(), 2)
        tile1 = Tile.objects.get(easting=-8873000, northing=5435000)
        self.assertEqual(tile1.country, self.country)
        tile2 = Tile.objects.get(easting=-8893000, northing=5435000)
        self.assertEqual(tile2.country, self.country)

        self.assertEqual(Contribution.objects.all().count(), 3)
        contribution1 = Contribution.objects.filter(tile=tile1).get()
        self.assertEqual(contribution1.observations, 200)

        self.assertEqual(Contribution.objects.filter(tile=tile2).count(), 2)
        for contribution in Contribution.objects.filter(tile=tile2):
            self.assertEqual(contribution.observations, 100)

    def test_invalid_data_returns_400(self):
        observation_data = {
            'items': [
                {
                    'time': 'asdf',
                    'tile_easting_m': 'asdf',
                    'tile_northing_m': 'asdf',
                    'observations': 'asdf',
                },
            ],
        }

        payload = json.dumps(observation_data)

        response = self.client.post(
            reverse('contributions-create'),
            payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Tile.objects.all().count(), 0)
        self.assertEqual(Contribution.objects.all().count(), 0)
        errors = response.data[0]
        self.assertIn('time', errors)
        self.assertIn('tile_easting_m', errors)
        self.assertIn('tile_northing_m', errors)
        self.assertIn('observations', errors)

    def test_submit_observations_with_gzipped_data(self):
        observation_data = {
            'items': [
                {
                    'time': time.time(),
                    'tile_easting_m': -8872100,
                    'tile_northing_m': 5435700,
                    'observations': 100,
                },
            ],
        }

        payload = gzip_compress(json.dumps(observation_data))

        response = self.client.post(
            reverse('contributions-create'),
            payload,
            content_type='application/json',
            headers={'Content-Encoding': 'gzip'},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tile.objects.all().count(), 1)
        self.assertEqual(Contribution.objects.all().count(), 1)

    def test_invalid_gzip_data_raises_400(self):
        response = self.client.post(
            reverse('contributions-create'),
            'asdf',
            content_type='application/json',
            headers={'Content-Encoding': 'gzip'},
        )

        self.assertEqual(response.status_code, 400)


class GetLeadersTests(TestCase):

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

        response = self.client.get(reverse('leaders-list'))
        self.assertEqual(response.status_code, 200)

        leaders_data = json.loads(response.content)
        self.assertEqual(leaders_data, {
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

        response = self.client.get(reverse('leaders-list'))
        self.assertEqual(response.status_code, 200)

        leaders_data = json.loads(response.content)
        self.assertEqual(len(leaders_data['results']), page_size)

        response = self.client.get(reverse('leaders-list'), {'page': 2})
        self.assertEqual(response.status_code, 200)

        leaders_data = json.loads(response.content)
        self.assertEqual(len(leaders_data['results']), 1)


class GetCountryLeadersTests(TestCase):

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

        leaders_data = json.loads(response.content)
        self.assertEqual(leaders_data, {
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
