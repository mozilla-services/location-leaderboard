import time
import json

import factory
from django.test import TestCase
from django.core.urlresolvers import reverse

from leaderboard.utils.compression import gzip_compress
from leaderboard.locations.models import Tile
from leaderboard.locations.tests.test_models import CountryTestMixin
from leaderboard.contributors.models import Contributor, Contribution


class ContributorFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Contributor {}'.format(n))
    email = factory.Sequence(
        lambda n: 'contributor{}@contribute.org'.format(n))

    class Meta:
        model = Contributor


# Create your tests here.
class ContributionTests(CountryTestMixin, TestCase):

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
