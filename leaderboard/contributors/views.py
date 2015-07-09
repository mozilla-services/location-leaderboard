from rest_framework.generics import CreateAPIView

from leaderboard.contributors.serializers import ContributionSerializer


class CreateContributionsView(CreateAPIView):
    """
    A POST API end point for submitting contributions.  Data arrives
    in the following JSON format:

    {
        'items': [
            {
                'tile_east': <int>,
                'tile_north': <int>,
                'observations': <int>,
            },
        ]
    }

    A successful POST returns a 201 HTTP Response.
    """
    serializer_class = ContributionSerializer

    def get_serializer(self, data=None, *args, **kwargs):
        if data:
            data = data.get('items', [])
        return super(CreateContributionsView, self).get_serializer(
            data=data, many=True, *args, **kwargs)
