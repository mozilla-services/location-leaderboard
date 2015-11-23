import json
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.models import Contributor, Contribution
from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.locations.models import Tile
from leaderboard.locations.tests.test_models import CountryFactory
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


class SubmitContributionTests(TestCase):

    def setUp(self):
        super(SubmitContributionTests, self).setUp()
        self.country = CountryFactory()
        self.contributor = ContributorFactory()

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
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Tile.objects.all().count(), 2)
        tile1 = Tile.objects.get(easting=-8873000, northing=5435000)
        self.assertEqual(tile1.country, self.country)
        tile2 = Tile.objects.get(easting=-8893000, northing=5435000)
        self.assertEqual(tile2.country, self.country)

        contributor_contributions = Contribution.objects.filter(
            contributor=self.contributor)
        self.assertEqual(contributor_contributions.count(), 3)
        contribution1 = contributor_contributions.filter(tile=tile1).get()
        self.assertEqual(contribution1.observations, 200)

        self.assertEqual(
            contributor_contributions.filter(tile=tile2).count(), 2)
        for contribution in contributor_contributions.filter(tile=tile2):
            self.assertEqual(contribution.observations, 100)

    def test_missing_authentication_token_returns_401(self):
        response = self.client.post(
            reverse('contributions-create'),
            '',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)

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
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
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
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
            HTTP_CONTENT_ENCODING='gzip',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tile.objects.all().count(), 1)
        self.assertEqual(Contribution.objects.all().count(), 1)

    def test_invalid_gzip_data_raises_400(self):
        response = self.client.post(
            reverse('contributions-create'),
            'asdf',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
            HTTP_CONTENT_ENCODING='gzip',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('gzip error', response.content)


class UpdateContributorTests(TestCase):

    def setUp(self):
        super(UpdateContributorTests, self).setUp()
        self.contributor = ContributorFactory()

    def test_update_contributor_saves_to_db(self):
        new_name = 'new name'

        response = self.client.patch(
            reverse('contributors-detail', kwargs={
                'uid': self.contributor.uid,
            }),
            json.dumps({'name': new_name}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
        )

        self.assertEquals(response.status_code, 200)

        response_data = json.loads(response.content)
        self.assertEqual(response_data, {u'name': unicode(new_name)})

        contributor = Contributor.objects.get(id=self.contributor.id)
        self.assertEqual(contributor.name, new_name)

    def test_update_contributor_cant_edit_another_contributor(self):
        contributor2 = ContributorFactory()
        new_name = 'new name'

        response = self.client.patch(
            reverse('contributors-detail', kwargs={'uid': contributor2.uid}),
            json.dumps({'name': new_name}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
        )

        self.assertEquals(response.status_code, 403)

    def test_update_contributor_doesnt_update_disallowed_field(self):
        old_access_token = self.contributor.access_token

        response = self.client.patch(
            reverse('contributors-detail', kwargs={
                'uid': self.contributor.uid,
            }),
            json.dumps({'access_token': 'asdf'}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(
                self.contributor.access_token),
        )

        self.assertEqual(response.status_code, 200)

        contributor = Contributor.objects.get(id=self.contributor.id)
        self.assertEqual(contributor.access_token, old_access_token)
