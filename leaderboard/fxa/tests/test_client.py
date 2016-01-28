import uuid
import json

import mock
from django.conf import settings
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

    def set_mock_response(self, mock, status_code=200, data=''):
        response = mock.MagicMock()
        response.status_code = status_code
        response.content = json.dumps(data)
        mock.return_value = response

    def setup_auth_call(self):
        fxa_auth_data = {
            'access_token': uuid.uuid4().hex,
            'auth_at': 123,
            'expires_in': 123,
            'scope': settings.FXA_SCOPE,
            'token_type': 'bearer'
        }

        self.set_mock_response(self.mock_post, data=fxa_auth_data)

        return fxa_auth_data

    def setup_verify_call(self, uid=None, client_id=None):
        fxa_verify_data = {
            'user': uid or uuid.uuid4().hex,
            'client_id': client_id or settings.FXA_CLIENT_ID,
            'scope': ['profile:email', 'profile:avatar'],
            'email': 'foo@example.com'
        }

        self.set_mock_response(self.mock_post, data=fxa_verify_data)

        return fxa_verify_data

    def setup_profile_call(self):
        fxa_profile_data = {
            'uid': uuid.uuid4().hex,
        }

        self.set_mock_response(self.mock_get, data=fxa_profile_data)

        return fxa_profile_data


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

    def test_get_refresh_token_returns_token(self):
        authorization_data = {
            'access_token': 'abcdef',
            'expires_in': 123,
            'scope': 'profile',
            'token_type': 'bearer'
        }

        response = mock.MagicMock()
        response.content = json.dumps(authorization_data)
        response.status_code = 200
        self.mock_post.return_value = response

        response_data = self.fxa_client.refresh_authorization_token('asdf')

        self.assertEqual(response_data, authorization_data)

    def test_verify_access_token_returns_verification_data(self):
        verify_data = {
            'user': '5901bd09376fadaa076afacef5251b6a',
            'client_id': '45defeda038a1c92',
            'scope': ['profile:email', 'profile:avatar'],
            'email': 'foo@example.com'
        }

        response = mock.MagicMock()
        response.content = json.dumps(verify_data)
        response.status_code = 200
        self.mock_post.return_value = response

        response_data = self.fxa_client.verify_token('asdf')

        self.assertEqual(response_data, verify_data)

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
