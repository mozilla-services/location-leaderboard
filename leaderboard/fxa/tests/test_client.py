import json

import mock
from django.test import TestCase

from leaderboard.fxa.client import FXAClientMixin, FXAException


class MockRequestTestMixin(object):

    def setUp(self):
        super(MockRequestTestMixin, self).setUp()

        mock_get_patcher = mock.patch('leaderboard.fxa.client.requests.get')
        self.mock_get = mock_get_patcher.start()
        self.addCleanup(mock_get_patcher.stop)

        mock_post_patcher = mock.patch('leaderboard.fxa.client.requests.post')
        self.mock_post = mock_post_patcher.start()
        self.addCleanup(mock_post_patcher.stop)


class TestFXAClient(FXAClientMixin, MockRequestTestMixin, TestCase):

    def test_get_authorization_token_returns_token(self):
        authorization_data = {
            'access_token': 'abcdef',
            'auth_at': 123,
            'expires_in': 123,
            'scope': 'profile',
            'token_type': 'bearer'
        }

        response = mock.MagicMock()
        response.content = json.dumps(authorization_data)
        response.status_code = 200
        self.mock_post.return_value = response

        response_data = self.fxa_client.get_authorization_token('asdf')

        self.assertEqual(response_data, authorization_data)

    def test_get_profile_data_returns_profile(self):
        profile_data = {
            'email': 'email@-example.com',
            'uid': '92e70a0155544210a787f98a4a22f6e2'
        }

        response = mock.MagicMock()
        response.content = json.dumps(profile_data)
        response.status_code = 200
        self.mock_get.return_value = response

        response_data = self.fxa_client.get_profile_data('asdf')

        self.assertEqual(response_data, profile_data)

    def test_non_200_status_raises_FXAException(self):
        response = mock.MagicMock()
        response.status_code = 400
        self.mock_post.return_value = response

        with self.assertRaises(FXAException):
            self.fxa_client._parse_response(response)

    def test_invalid_json_raises_FXAException(self):
        response = mock.MagicMock()
        response.status_code = 200
        response.content = ''
        self.mock_post.return_value = response

        with self.assertRaises(FXAException):
            self.fxa_client._parse_response(response)
