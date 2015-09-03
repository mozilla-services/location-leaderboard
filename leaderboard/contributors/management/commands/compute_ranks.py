from django.core.management.base import BaseCommand
from leaderboard.contributors.models import ContributorRank


class Command(BaseCommand):
    help = """
        Precompute each contributors observations
        and rank globally and per country
    """

    def handle(self, *args, **options):
        ContributorRank.compute_ranks()
