import json
import urllib
import urlparse

import requests
from django.core.urlresolvers import reverse
from django.conf import settings


def get_fxa_login_url(base_url):
    """
    Construct a URL which will trigger an Oauth login flow inside FXA.
    """
    login_params = {
        'action': 'signin',
        'access_type': 'offline',
        'client_id': settings.FXA_CLIENT_ID,
        'scope': settings.FXA_SCOPE,
        'state': 99,
        'redirect_uri': urlparse.urljoin(base_url, reverse('fxa-redirect')),
    }

    login_url = '{url}?{query}'.format(
        url=urlparse.urljoin(
            settings.FXA_OAUTH_URI,
            '/v1/authorization',
        ),
        query=urllib.urlencode(login_params),
    )

    return login_url


class FXAException(Exception):
    """
    An exception raised by an FXA client instance if
    it fails to make a successful request to the FXA servers.
    """
    pass


class FXAClientMixin(object):
    """
    An object which has an FXA client.
    """

    def __init__(self, *args, **kwargs):
        self.fxa_client = FXAClient()
        super(FXAClientMixin, self).__init__(*args, **kwargs)


class FXAClient(object):
    """
    An FXA client which allows you to communicate with the
    FXA oauth and profile services.
    """

    def _parse_response(self, response):
        """
        Ensure that a response returned status 200 then parse
        and return its JSON contents.
        """
        if response.status_code != 200:
            raise FXAException('Request Error: {}'.format(response.content))

        try:
            json_data = json.loads(response.content)
        except ValueError, e:
            raise FXAException('JSON Error: {}'.format(e))

        return json_data

    def get_authorization_token(self, code):
        """
        Exchange a temporary auth code received during a successful login
        redirect for a long lived access token.

        Example response:

        {
            'access_token': 'asdf',
            'refresh_token': 'asdf',
            'auth_at': 1438019181,
            'expires_in': 172800,
            'scope': 'profile',
            'token_type': 'bearer'
        }
        """
        params = {
            'grant_type': 'authorization_code',
            'client_id': settings.FXA_CLIENT_ID,
            'client_secret': settings.FXA_SECRET,
            'code': code,
        }

        token_url = urlparse.urljoin(settings.FXA_OAUTH_URI, 'v1/token')
        response = requests.post(token_url, data=json.dumps(params))

        return self._parse_response(response)

    def refresh_authorization_token(self, refresh_token):
        """
        Exchange a refresh token for a new access token.

        Example response:

        {
            'access_token': 'asdf',
            'expires_in': 1209600,
            'scope': 'profile',
            'token_type': 'bearer'}
        }
        """
        params = {
            'grant_type': 'refresh_token',
            'client_id': settings.FXA_CLIENT_ID,
            'client_secret': settings.FXA_SECRET,
            'scope': settings.FXA_SCOPE,
            'refresh_token': refresh_token,
        }

        token_url = urlparse.urljoin(settings.FXA_OAUTH_URI, 'v1/token')
        response = requests.post(token_url, data=json.dumps(params))

        return self._parse_response(response)

    def get_profile_data(self, access_token):
        """
        Retrieve the profile details for a user given a valid access_token.

        Example response:

        {
            'email': 'email@-example.com',
            'uid': '92e70a0155544210a787f98a4a22f6e2'
        }
        """
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }

        profile_url = urlparse.urljoin(settings.FXA_PROFILE_URI, 'v1/profile')
        response = requests.get(profile_url, headers=headers)

        return self._parse_response(response)
