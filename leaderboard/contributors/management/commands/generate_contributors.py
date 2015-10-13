import datetime
import random

from django.core.management.base import BaseCommand

from leaderboard.locations.models import Country
from leaderboard.locations.tests.test_models import TileFactory
from leaderboard.contributors.models import Contribution
from leaderboard.contributors.tests.test_models import ContributorFactory


class Command(BaseCommand):
    help = """
        Generate fictitious contributors and contributions
        for testing purposes.
    """

    def add_arguments(self, parser):
        parser.add_argument('num_contributors', type=int)

    def handle(self, *args, **options):
        countries = Country.objects.all()

        for num_contributor in range(options['num_contributors']):
            contributor = ContributorFactory()

            for contribution_i in range(random.randint(3, 10)):
                country = random.choice(countries)
                contribution = Contribution.objects.create(
                    contributor=contributor,
                    date=datetime.date.today(),
                    tile=TileFactory(country=country),
                    observations=random.randint(100, 1000),
                )
                print contribution
