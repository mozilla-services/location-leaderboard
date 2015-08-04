from django.core.urlresolvers import reverse
from django.test import TestCase


class LandingViewTests(TestCase):

    def test_landing_page_renders(self):
        response = self.client.get(reverse('home-landing'))
        self.assertEqual(response.status_code, 200)
