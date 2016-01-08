from uuid import uuid4

from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from leaderboard.contributors.models import Contributor
from leaderboard.fxa.authenticator import OAuthTokenAuthentication
from leaderboard.fxa.client import (
    get_fxa_login_url,
    FXAClientMixin,
    FXAException,
)


class FXALoginView(View):

    def get(self, request):
        base_url = request.build_absolute_uri('/')
        return redirect(get_fxa_login_url(base_url))


class FXAConfigView(APIView):

    def get(self, request):
        return Response(
            {
                'client_id': settings.FXA_CLIENT_ID,
                'scopes': settings.FXA_SCOPE,
                'oauth_uri': settings.FXA_OAUTH_URI,
                'profile_uri': settings.FXA_PROFILE_URI,
                'redirect_uri': request.build_absolute_uri(
                    reverse('fxa-redirect')),
            },
            content_type='application/json',
        )


class FXARedirectView(FXAClientMixin, APIView):

    def get(self, request):
        code = request.GET.get('code', None)

        if code is None:
            raise ValidationError('Unable to determine access code.')

        try:
            fxa_auth_data = self.fxa_client.get_authorization_token(code)
        except FXAException:
            raise ValidationError(
                'Unable to communicate with Firefox Accounts.')

        access_token = fxa_auth_data.get('access_token', None)

        if access_token is None:
            raise ValidationError(
                'Unable to retrieve Firefox Accounts Access Token.')

        try:
            fxa_profile_data = self.fxa_client.get_profile_data(access_token)
        except FXAException:
            raise ValidationError(
                'Unable to retrieve Firefox Accounts Profile.')

        fxa_uid = fxa_profile_data.get('uid', None)

        if fxa_uid is None:
            raise ValidationError('Unable to retrieve Firefox Accounts UID.')

        contributor, created = Contributor.objects.get_or_create(
            fxa_uid=fxa_uid,
        )

        if created:
            contributor.uid = uuid4().hex
            contributor.save()

        return Response(
            {
                'leaderboard_uid': contributor.uid,
                'fxa_uid': fxa_uid,
                'fxa_auth_data': fxa_auth_data,
            },
            content_type='application/json',
        )


class FXARefreshView(FXAClientMixin, APIView):
    authentication_classes = (OAuthTokenAuthentication,)

    def post(self, request):
        refresh_token = request.POST.get('refresh_token', None)

        if refresh_token is None:
            raise ValidationError('Unable to determine refresh token.')

        try:
            fxa_auth_data = self.fxa_client.refresh_authorization_token(
                refresh_token)
        except FXAException:
            raise ValidationError(
                'Unable to communicate with Firefox Accounts.')

        return Response(fxa_auth_data, content_type='application/json')
