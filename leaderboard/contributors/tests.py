import json

import factory
from django.test import TestCase
from django.core.urlresolvers import reverse

from leaderboard.locations.models import Tile
from leaderboard.locations.tests import CountryTestMixin
from leaderboard.contributors.models import Contributor, Contribution


class ContributorFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Contributor {}'.format(n))
    email = factory.Sequence(
        lambda n: 'contributor{}@contribute.org'.format(n))

    class Meta:
        model = Contributor


# Create your tests here.
class ContributionTests(CountryTestMixin, TestCase):

    def test_submit_observations(self):
        observation_data = {
            'items': [
                {
                    'tile_east': -8872100,
                    'tile_north': 5435700,
                    'observations': 100,
                },
                {
                    'tile_east': -8872100,
                    'tile_north': 5435700,
                    'observations': 100,
                },
                {
                    'tile_east': -8892100,
                    'tile_north': 5435700,
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
        tile1 = Tile.objects.get(east=-8873000, north=5435000)
        tile2 = Tile.objects.get(east=-8893000, north=5435000)
        self.assertEqual(tile1.country, self.country)
        self.assertEqual(tile2.country, self.country)

        self.assertEqual(Contribution.objects.all().count(), 3)
        self.assertEqual(Contribution.objects.filter(tile=tile1).count(), 2)
        self.assertEqual(Contribution.objects.filter(tile=tile2).count(), 1)
