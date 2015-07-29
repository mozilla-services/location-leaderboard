import json
import urlparse

import requests
from django.conf import settings


class FXAException(Exception):
    """
    An exception raised by an FXA client instance if
    it fails to make a successful request to the FXA servers.
    """
    pass


def get_fxa_client():
    """
    Return an FXA client using the parameters set in your
    project Django settings.
    """
    return FXAClient(
        oauth_uri=settings.FXA_OAUTH_URI,
        profile_uri=settings.FXA_PROFILE_URI,
        client_id=settings.FXA_CLIENT_ID,
        client_secret=settings.FXA_SECRET,
    )


class FXAClientMixin(object):
    """
    An object which has an FXA client.
    """

    def __init__(self, *args, **kwargs):
        self.fxa_client = get_fxa_client()
        super(FXAClientMixin, self).__init__(*args, **kwargs)


class FXAClient(object):
    """
    An FXA client which allows you to communicate with the
    FXA oauth and profile services.
    """

    def __init__(self, oauth_uri, profile_uri, client_id, client_secret):
        self.oauth_uri = oauth_uri
        self.profile_uri = profile_uri
        self.client_id = client_id
        self.client_secret = client_secret

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
            'auth_at': 1438019181,
            'expires_in': 172800,
            'scope': 'profile',
            'token_type': 'bearer'
        }
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }

        token_url = urlparse.urljoin(self.oauth_uri, 'token')
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

        profile_url = urlparse.urljoin(self.profile_uri, 'profile')
        response = requests.get(profile_url, headers=headers)

        return self._parse_response(response)
