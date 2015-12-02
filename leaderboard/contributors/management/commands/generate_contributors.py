import datetime
import random

from django.core.management.base import BaseCommand

from leaderboard.locations.models import Country
from leaderboard.locations.tests.test_models import TileFactory
from leaderboard.contributors.models import Contributor, Contribution
from leaderboard.contributors.tests.test_models import ContributorFactory


class Command(BaseCommand):
    help = """
        Generate fictitious contributors and contributions
        for testing purposes.
    """

    def add_arguments(self, parser):
        parser.add_argument('new_contributors', type=int)
        parser.add_argument('new_contributions', type=int)

    def handle(self, *args, **options):
        countries = Country.objects.all()

        for num_contributor in range(options['new_contributors']):
            ContributorFactory()

        contributors = list(Contributor.objects.all())

        new_contributions = []

        for contribution_i in range(options['new_contributions']):
            new_contributions.append(Contribution(
                contributor=random.choice(contributors),
                date=datetime.date.today(),
                tile=TileFactory(country=random.choice(countries)),
                observations=random.randint(100, 1000),
            ))

        Contribution.objects.bulk_create(new_contributions)
