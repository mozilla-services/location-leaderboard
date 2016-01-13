import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase


class LandingViewTests(TestCase):

    def test_landing_page_renders(self):
        response = self.client.get(reverse('home-landing'))
        self.assertEqual(response.status_code, 200)


class VersionViewTests(TestCase):

    def test_version_view_returns_git_settings(self):
        git_settings = {
            'commit': 'abcdef',
            'source': 'git/repo/path',
            'tag': 'test-0.1',
            'version': '0.1',
        }

        with self.settings(**git_settings):
            response = self.client.get(reverse('home-version'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            version_data = json.loads(response.content)
            self.assertEqual(version_data, {
                'commit': settings.GIT_COMMIT,
                'source':  settings.GIT_SOURCE,
                'tag': settings.GIT_TAG,
                'version': settings.GIT_VERSION,
            })
