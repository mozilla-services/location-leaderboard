import random

import factory
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.test import TestCase

from leaderboard.locations.models import Country


class CountryFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Country {}'.format(n))
    area = factory.LazyAttribute(lambda o: random.randint(1000, 9999999))
    pop2005 = factory.LazyAttribute(lambda o: random.randint(1000, 999999))
    fips = factory.Sequence(lambda n: str(n))
    iso2 = factory.Sequence(lambda n: str(n))
    iso3 = factory.Sequence(lambda n: str(n))
    un = factory.Sequence(lambda n: n)
    region = factory.Sequence(lambda n: n)
    subregion = factory.Sequence(lambda n: n)
    geometry = factory.Sequence(lambda n: MultiPolygon([
        Polygon([
            Point(n, n),
            Point(n, n+1),
            Point(n+1, n),
            Point(n+1, n+1),
            Point(n, n),
        ]),
    ]))

    class Meta:
        model = Country


class TestCountryManager(TestCase):

    def test_nearest_to_point_returns_nearest_country(self):
        country1 = CountryFactory.build()
        country1.save()

        country2 = CountryFactory.build()
        country2.geometry = MultiPolygon([
            Polygon([
                Point(1000, 1000),
                Point(1000, 1001),
                Point(1001, 1000),
                Point(1001, 1001),
                Point(1000, 1000),
            ]),
        ])
        country2.save()

        point = Point(0, 0)
        nearest_country = Country.objects.nearest_to_point(point)
        self.assertEqual(nearest_country, country1)
