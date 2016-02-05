from rest_framework.generics import CreateAPIView

from leaderboard.fxa.authenticator import OAuthTokenAuthentication
from leaderboard.contributors.serializers import ContributionSerializer


class CreateContributionsView(CreateAPIView):
    """
    Create a contribution from user submitted data.
    """
    authentication_classes = (OAuthTokenAuthentication,)
    serializer_class = ContributionSerializer

    def get_serializer(self, data=None, *args, **kwargs):
        if data:
            data = data.get('items', [])

        return super(CreateContributionsView, self).get_serializer(
            data=data, many=True, *args, **kwargs)
