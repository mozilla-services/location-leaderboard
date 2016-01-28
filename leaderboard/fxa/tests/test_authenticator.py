import mock
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from leaderboard.contributors.models import Contributor
from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.fxa.authenticator import OAuthTokenAuthentication
from leaderboard.fxa.tests.test_client import MockRequestTestMixin


class TestOAuthTokenAuthentication(MockRequestTestMixin, TestCase):

    def test_returns_none_if_missing_token(self):
        request = mock.MagicMock()
        request.META = {}

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_raises_authenticationfailed_if_malformed_header(self):
        request = mock.MagicMock()
        request.META = {'HTTP_AUTHORIZATION': 'invalid'}

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_raises_authenticationfailed_if_token_unknown(self):
        self.set_mock_response(self.mock_get, status_code=400)

        request = mock.MagicMock()
        request.META = {'HTTP_AUTHORIZATION': 'Bearer abc'}

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_raises_authenticationfailed_if_uid_missing(self):
        fxa_client_id = 'client id'

        with self.settings(FXA_CLIENT_ID=fxa_client_id):
            self.set_mock_response(self.mock_post, data={
                'client_id': fxa_client_id,
            })

            request = mock.MagicMock()
            request.META = {'HTTP_AUTHORIZATION': 'Bearer abc'}

            with self.assertRaises(AuthenticationFailed):
                OAuthTokenAuthentication().authenticate(request)

    def test_raises_authenticationfailed_if_no_contributor_found(self):
        self.setup_verify_call()

        request = mock.MagicMock()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer asdf',
        }

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_authentication_fails_if_client_id_does_not_match(self):
        fxa_profile_data = self.setup_profile_call()
        self.setup_verify_call(
            uid=fxa_profile_data['uid'], client_id='wrong id')

        request = mock.MagicMock()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer asdf',
        }

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_authentication_fails_if_unable_to_retrieve_profile_data(self):
        fxa_verify_data = self.setup_verify_call()

        ContributorFactory(fxa_uid=fxa_verify_data['user'])

        request = mock.MagicMock()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer asdf',
        }

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_parses_header_and_returns_contributor(self):
        fxa_profile_data = self.setup_profile_call()
        self.setup_verify_call(uid=fxa_profile_data['uid'])

        contributor = ContributorFactory(fxa_uid=fxa_profile_data['uid'])

        request = mock.MagicMock()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer asdf',
        }

        user, token = OAuthTokenAuthentication().authenticate(request)

        self.assertEqual(user, contributor)

    def test_authenticator_updates_display_name(self):
        contributor = ContributorFactory()

        fxa_profile_data = {
            'uid': contributor.fxa_uid,
            'displayName': 'new name',
        }

        self.set_mock_response(self.mock_get, data=fxa_profile_data)

        self.setup_verify_call(uid=fxa_profile_data['uid'])

        request = mock.MagicMock()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer asdf',
        }

        user, token = OAuthTokenAuthentication().authenticate(request)

        contributor = Contributor.objects.get()

        self.assertEqual(contributor.name, fxa_profile_data['displayName'])
