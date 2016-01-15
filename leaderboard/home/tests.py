import json

import mock
from django.core.urlresolvers import reverse
from django.db import OperationalError
from django.test import TestCase


class LandingViewTests(TestCase):

    def test_landing_page_renders(self):
        response = self.client.get(reverse('home-landing'))
        self.assertEqual(response.status_code, 200)


class VersionViewTests(TestCase):

    def test_version_view_returns_git_settings(self):
        git_settings = {
            'GIT_COMMIT': 'abcdef',
            'GIT_SOURCE': 'git/repo/path',
            'GIT_TAG': 'test-0.1',
            'GIT_VERSION': '0.1',
        }

        with self.settings(**git_settings):
            response = self.client.get(reverse('home-version'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            version_data = json.loads(response.content)
            self.assertEqual(version_data, {
                'commit': git_settings['GIT_COMMIT'],
                'source': git_settings['GIT_SOURCE'],
                'tag': git_settings['GIT_TAG'],
                'version': git_settings['GIT_VERSION'],
            })


class HearbeatViewTests(TestCase):

    def test_heartbeat_view_returns_200_if_able_to_reach_db(self):
        response = self.client.get(reverse('home-heartbeat'))
        self.assertEqual(response.status_code, 200)

    @mock.patch('leaderboard.home.views.connections')
    def test_heartbeat_view_fails_if_unable_to_reach_db(self, mocked_conn):
        mocked_conn['default'].cursor.side_effect = OperationalError

        response = self.client.get(reverse('home-heartbeat'))
        self.assertEqual(response.status_code, 400)
