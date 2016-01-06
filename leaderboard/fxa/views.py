from uuid import uuid4

from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from leaderboard.contributors.models import Contributor
from leaderboard.fxa.client import FXAClientMixin, FXAException


class FXAConfigView(APIView):

    def get(self, request):
        return Response(
            {
                'client_id': settings.FXA_CLIENT_ID,
                'scopes': settings.FXA_SCOPES,
                'oauth_uri': settings.FXA_OAUTH_URI,
                'profile_uri': settings.FXA_PROFILE_URI,
                'redirect_uri': request.build_absolute_uri(
                    reverse('fxa-redirect')),
            },
            content_type='application/json',
        )


class FXARedirectView(FXAClientMixin, APIView):

    def get(self, request):
        code = request.GET.get('code', '')

        if not code:
            raise ValidationError('Unable to determine access code.')

        try:
            token_data = self.fxa_client.get_authorization_token(code)
        except FXAException:
            raise ValidationError(
                'Unable to communicate with Firefox Accounts.')

        access_token = token_data.get('access_token', None)

        if not access_token:
            raise ValidationError('Unable to retrieve access token.')

        contributor, created = Contributor.objects.get_or_create(
            access_token=access_token,
            uid=uuid4().hex,
        )

        return Response(
            {
                'access_token': access_token,
                'uid': contributor.uid,
            },
            content_type='application/json',
        )
