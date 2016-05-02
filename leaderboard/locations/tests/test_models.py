import random

import factory
from django.contrib.gis.geos import Point, Polygon, MultiPolygon

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
            Point(n+1, n+1),
            Point(n+1, n),
            Point(n, n),
        ]),
    ]))

    class Meta:
        model = Country
