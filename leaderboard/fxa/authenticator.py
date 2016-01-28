import re

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import (
    get_authorization_header,
    BaseAuthentication,
)

from leaderboard.fxa.client import FXAClientMixin, FXAException
from leaderboard.contributors.models import Contributor


# A regex which matches against a Bearer token
# http://self-issued.info/docs/draft-ietf-oauth-v2-bearer.html#authz-header
FXA_ACCESS_TOKEN_RE = re.compile('Bearer\s+(?P<token>[a-zA-Z0-9._~+\/\-=]+)')


class OAuthTokenAuthentication(FXAClientMixin, BaseAuthentication):
    """
    Simple token based authentication for OAuth v2.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:
        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a

    http://self-issued.info/docs/draft-ietf-oauth-v2-bearer.html#authz-header
    """

    def authenticate(self, request):
        auth_header = get_authorization_header(request)

        if not auth_header:
            msg = 'Missing token header.'
            raise AuthenticationFailed(msg)

        match = FXA_ACCESS_TOKEN_RE.match(auth_header)

        if not match:
            msg = 'Invalid token header. Must match: `Bearer <token>`.'
            raise AuthenticationFailed(msg)

        access_token = match.groupdict()['token']

        try:
            verify_data = self.fxa_client.verify_token(access_token)
        except FXAException, e:
            msg = (
                'Unable to verify access token '
                'with Firefox Accounts: {}'
            ).format(e)
            raise AuthenticationFailed(msg)

        client_id = verify_data.get('client_id', None)

        if client_id != settings.FXA_CLIENT_ID:
            msg = (
                'Provided access token is not '
                'valid for use with this service.'
            )
            raise AuthenticationFailed(msg)

        fxa_uid = verify_data.get('user', None)

        if fxa_uid is None:
            msg = 'Unable to retrieve Firefox Accounts user id.'
            raise AuthenticationFailed(msg)

        try:
            contributor = Contributor.objects.get(fxa_uid=fxa_uid)
        except Contributor.DoesNotExist:
            msg = 'No contributor found.'
            raise AuthenticationFailed(msg)

        try:
            profile_data = self.fxa_client.get_profile_data(access_token)
        except FXAException, e:
            msg = (
                'Unable to retrieve profile '
                'data from Firefox Accounts: {}'
            ).format(e)
            raise AuthenticationFailed(msg)

        display_name = profile_data.get('displayName', None)
        if display_name is not None and display_name != contributor.name:
            contributor.name = display_name
            contributor.save()

        return (
            contributor,
            {
                'access_token': access_token,
                'profile_data': profile_data,
            },
        )

    def authenticate_header(self, request):
        return 'Token'
