import datetime
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.contributors.models import Contribution, ContributorRank
from leaderboard.contributors.tests.test_models import ContributorFactory
from leaderboard.locations.tests.test_models import CountryFactory


class TestCountryListVIew(TestCase):

    def test_list_countries_returns_country_data(self):
        today = datetime.date.today()

        countries = [CountryFactory() for i in range(3)]

        # A country with no contributions should not appear
        # in the results
        CountryFactory()

        for country in countries:
            for contributor_i in range(3):
                contributor = ContributorFactory()

                for contribution_i in range(10):
                    Contribution.objects.create(
                        contributor=contributor,
                        country=country,
                        date=today,
                        observations=1,
                    )

        ContributorRank.compute_ranks()

        response = self.client.get(reverse('countries-list'))

        self.assertEqual(response.status_code, 200)

        countries_data = json.loads(response.content)
        self.assertEqual(len(countries_data), len(countries))

        for country in countries:
            self.assertIn({
                'iso2': country.iso2,
                'name': country.name,
                'observations': 30,
                'leaders_url': reverse(
                    'leaders-country-list',
                    kwargs={'country_id': country.iso2},
                ),
            }, countries_data)
