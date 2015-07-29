from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from leaderboard.fxa.client import FXAClientMixin, FXAException


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

        return Response(
            {'access_token': access_token},
            content_type='application/json',
        )
