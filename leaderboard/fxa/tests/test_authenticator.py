import mock
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.fxa.authenticator import OAuthTokenAuthentication


class TestOAuthTokenAuthentication(TestCase):

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
        request = mock.MagicMock()
        request.META = {'HTTP_AUTHORIZATION': 'Bearer abc'}

        with self.assertRaises(AuthenticationFailed):
            OAuthTokenAuthentication().authenticate(request)

    def test_parses_header_and_returns_contributor(self):
        contributor = ContributorFactory()

        request = mock.MagicMock()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(contributor.access_token)
        }

        user, token = OAuthTokenAuthentication().authenticate(request)

        self.assertEqual(user, contributor)
        self.assertEqual(token, contributor.access_token)
