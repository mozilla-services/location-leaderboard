import json

import mock
from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.models import Contributor
from leaderboard.fxa.tests.test_client import MockRequestTestMixin


class TestFXARedirectView(MockRequestTestMixin, TestCase):

    def test_successful_redirect_returns_access_code(self):
        access_token = 'abcdef'
        authorization_data = {
            'access_token': access_token,
            'auth_at': 123,
            'expires_in': 123,
            'scope': 'profile',
            'token_type': 'bearer'
        }
        fxa_response = mock.MagicMock()
        fxa_response.status_code = 200
        fxa_response.content = json.dumps(authorization_data)
        self.mock_post.return_value = fxa_response

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        self.assertEqual(
            response_data,
            {'access_token': access_token},
        )

        contributor = Contributor.objects.get()
        self.assertEqual(contributor.access_token, access_token)

    def test_missing_code_raises_400(self):
        response = self.client.get(reverse('fxa-redirect'))

        self.assertEqual(response.status_code, 400)

    def test_fxa_error_raises_400(self):
        fxa_response = mock.MagicMock()
        fxa_response.status_code = 400
        self.mock_post.return_value = fxa_response

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 400)

    def test_empty_access_token_raises_400(self):
        fxa_response = mock.MagicMock()
        fxa_response.status_code = 200
        fxa_response.content = json.dumps({})
        self.mock_post.return_value = fxa_response

        response = self.client.get(reverse('fxa-redirect'), {'code': 'asdf'})

        self.assertEqual(response.status_code, 400)

    def test_multiple_contributors_signin_creates_multiple_contributors(self):
        access_token1 = 'access1'
        authorization_data = {
            'access_token': access_token1,
            'auth_at': 123,
            'expires_in': 123,
            'scope': 'profile',
            'token_type': 'bearer'
        }
        fxa_response = mock.MagicMock()
        fxa_response.status_code = 200
        fxa_response.content = json.dumps(authorization_data)
        self.mock_post.return_value = fxa_response

        response = self.client.get(reverse('fxa-redirect'), {'code': 'code1'})

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        self.assertEqual(
            response_data,
            {'access_token': access_token1},
        )

        self.assertEqual(Contributor.objects.count(), 1)
        Contributor.objects.get(access_token=access_token1)

        access_token2 = 'access2'
        authorization_data = {
            'access_token': access_token2,
            'auth_at': 123,
            'expires_in': 123,
            'scope': 'profile',
            'token_type': 'bearer'
        }
        fxa_response = mock.MagicMock()
        fxa_response.status_code = 200
        fxa_response.content = json.dumps(authorization_data)
        self.mock_post.return_value = fxa_response

        response = self.client.get(reverse('fxa-redirect'), {'code': 'code2'})

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        self.assertEqual(
            response_data,
            {'access_token': access_token2},
        )

        self.assertEqual(Contributor.objects.count(), 2)
        Contributor.objects.get(access_token=access_token2)
