import json

import mock
from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.fxa.tests.test_client import MockRequestTestMixin


class TestFXARedirectView(MockRequestTestMixin, TestCase):

    def test_successful_redirect_returns_access_code(self):
        authorization_data = {
            'access_token': 'abcdef',
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
            {'access_token': authorization_data['access_token']},
        )

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
