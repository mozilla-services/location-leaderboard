import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from leaderboard.locations.tests.test_models import CountryTestMixin


class TestCountryListVIew(CountryTestMixin, TestCase):

    def test_list_countries_returns_json_and_200(self):
        response = self.client.get(reverse('countries-list'))

        self.assertEqual(response.status_code, 200)

        countries_data = json.loads(response.content)
        self.assertEqual(countries_data, [{
            'id': self.country.id,
            'name': self.country.name,
            'geometry': json.loads(self.country.geometry.geojson),
        }])
