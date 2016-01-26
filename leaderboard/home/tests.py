import mock
from django.core.urlresolvers import reverse
from django.db import OperationalError
from django.test import TestCase


class LandingViewTests(TestCase):

    def test_landing_page_renders(self):
        response = self.client.get(reverse('home-landing'))
        self.assertEqual(response.status_code, 200)


class HearbeatViewTests(TestCase):

    def test_heartbeat_view_returns_200_if_able_to_reach_db(self):
        response = self.client.get(reverse('home-heartbeat'))
        self.assertEqual(response.status_code, 200)

    @mock.patch('leaderboard.home.views.connections')
    def test_heartbeat_view_fails_if_unable_to_reach_db(self, mocked_conn):
        mocked_conn['default'].cursor.side_effect = OperationalError

        response = self.client.get(reverse('home-heartbeat'))
        self.assertEqual(response.status_code, 400)
