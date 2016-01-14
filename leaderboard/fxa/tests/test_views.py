import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.contributors.models import Contributor
from leaderboard.fxa.client import get_fxa_login_url
from leaderboard.fxa.tests.test_client import MockRequestTestMixin


class TestFXALoginView(TestCase):

    def test_login_view_redirects_to_fxa_url(self):
        test_settings = {
            'FXA_CLIENT_ID': 'fxa_client_id',
            'FXA_SCOPE': 'profile leaderboard',
            'FXA_OAUTH_URI': 'http://example.com/v1/oauth/',
            'FXA_PROFILE_URI': 'http://example.com/v1/profile/',
        }

        with self.settings(**test_settings):
            response = self.client.get(reverse('fxa-login'))

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.url, get_fxa_login_url('http://testserver/'))


class TestFXAConfigView(TestCase):

    def test_config_view_returns_fxa_settings(self):
        test_settings = {
            'FXA_CLIENT_ID': 'fxa_client_id',
            'FXA_SCOPE': 'profile leaderboard',
            'FXA_OAUTH_URI': 'http://example.com/v1/oauth/',
            'FXA_PROFILE_URI': 'http://example.com/v1/profile/',
        }

        with self.settings(**test_settings):
            response = self.client.get(reverse('fxa-config'))

            self.assertEqual(response.status_code, 200)

            response_data = json.loads(response.content)
            self.assertEqual(response_data, {
                'client_id': test_settings['FXA_CLIENT_ID'],
                'scopes': test_settings['FXA_SCOPE'],
                'oauth_uri': test_settings['FXA_OAUTH_URI'],
                'leaderboard_base_uri': 'http://testserver',
                'profile_uri': test_settings['FXA_PROFILE_URI'],
                'redirect_uri': 'http://testserver{path}'.format(
                    path=reverse('fxa-redirect')),
            })


class TestFXARedirectView(MockRequestTestMixin, TestCase):

    def test_successful_redirect_creates_contributor(self):
        fxa_auth_data = self.setup_auth_call()
        fxa_profile_data = self.setup_profile_call()

        self.assertEqual(Contributor.objects.count(), 0)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contributor.objects.count(), 1)

        contributor = Contributor.objects.get()

        response_data = json.loads(response.content)

        self.assertEqual(response_data, {
            'leaderboard_uid': contributor.uid,
            'fxa_uid': fxa_profile_data['uid'],
            'fxa_auth_data': fxa_auth_data,
        })

        self.assertEqual(contributor.fxa_uid, fxa_profile_data['uid'])
        self.assertTrue(contributor.uid is not None)

    def test_missing_code_raises_400(self):
        response = self.client.get(reverse('fxa-redirect'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Contributor.objects.count(), 0)

    def test_fxa_auth_error_raises_400(self):
        self.set_mock_response(self.mock_post, status_code=400)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 400)

    def test_fxa_profile_error_raises_400(self):
        self.setup_auth_call()
        self.set_mock_response(self.mock_get, status_code=400)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 400)

    def test_missing_uid_raises_400(self):
        self.setup_auth_call()

        fxa_profile_data = {
            'email': 'user@example.com',
        }

        self.set_mock_response(self.mock_get, data=fxa_profile_data)

        self.assertEqual(Contributor.objects.count(), 0)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Contributor.objects.count(), 0)

    def test_missing_access_token_raises_400(self):
        self.set_mock_response(self.mock_post, data={})

        self.assertEqual(Contributor.objects.count(), 0)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 400)

    def test_new_signin_for_existing_contributor_reuses_contributor(self):
        self.setup_auth_call()
        fxa_profile_data = self.setup_profile_call()

        self.assertEqual(Contributor.objects.count(), 0)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contributor.objects.count(), 1)

        contributor = Contributor.objects.get()

        self.assertEqual(contributor.fxa_uid, fxa_profile_data['uid'])
        self.assertTrue(contributor.uid is not None)

        self.setup_auth_call()

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contributor.objects.count(), 1)

        contributor = Contributor.objects.get()

        self.assertEqual(contributor.fxa_uid, fxa_profile_data['uid'])
        self.assertTrue(contributor.uid, contributor.uid)

    def test_multiple_contributors_signin_creates_multiple_contributors(self):
        self.setup_auth_call()
        fxa_profile_data1 = self.setup_profile_call()

        self.assertEqual(Contributor.objects.count(), 0)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contributor.objects.count(), 1)

        contributor = Contributor.objects.get(fxa_uid=fxa_profile_data1['uid'])

        self.assertEqual(contributor.fxa_uid, fxa_profile_data1['uid'])
        self.assertTrue(contributor.uid is not None)

        self.setup_auth_call()
        fxa_profile_data2 = self.setup_profile_call()

        self.assertEqual(Contributor.objects.count(), 1)

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contributor.objects.count(), 2)

        contributor = Contributor.objects.get(fxa_uid=fxa_profile_data2['uid'])

        self.assertEqual(contributor.fxa_uid, fxa_profile_data2['uid'])
        self.assertTrue(contributor.uid is not None)


class TestFXARefreshView(MockRequestTestMixin, TestCase):

    def setUp(self):
        super(TestFXARefreshView, self).setUp()
        fxa_profile_data = self.setup_profile_call()
        self.contributor = ContributorFactory(fxa_uid=fxa_profile_data['uid'])

    def test_successful_refresh_returns_new_token(self):
        fxa_auth_data = self.setup_auth_call()

        response = self.client.post(
            reverse('fxa-refresh'),
            data={'refresh_token': 'asdf'},
            HTTP_AUTHORIZATION='Bearer asdf',
        )

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        self.assertEqual(response_data, fxa_auth_data)

    def test_missing_access_token_raises_403(self):
        response = self.client.post(
            reverse('fxa-refresh'),
            data={'refresh_token': 'asdf'},
        )

        self.assertEqual(response.status_code, 401)

    def test_invalid_access_token_raises_403(self):
        self.set_mock_response(self.mock_get, status_code=400)

        response = self.client.post(
            reverse('fxa-refresh'),
            data={'refresh_token': 'asdf'},
            HTTP_AUTHORIZATION='Bearer asdf',
        )

        self.assertEqual(response.status_code, 401)

    def test_missing_refresh_token_raises_400(self):
        response = self.client.post(
            reverse('fxa-refresh'),
            data={},
            HTTP_AUTHORIZATION='Bearer asdf',
        )

        self.assertEqual(response.status_code, 400)

    def test_fxa_auth_error_raises_400(self):
        self.set_mock_response(self.mock_post, status_code=400)

        response = self.client.post(
            reverse('fxa-refresh'),
            data={'refresh_token': 'asdf'},
            HTTP_AUTHORIZATION='Bearer asdf',
        )

        self.assertEqual(response.status_code, 400)
