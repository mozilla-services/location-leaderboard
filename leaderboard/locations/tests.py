import uuid
import random

import factory
from django.test import TestCase

from leaderboard.locations.projected_geos import (
    ProjectedMultiPolygon,
    ProjectedPolygon,
    ProjectedPoint,
)
from leaderboard.locations.models import Country, Tile


class CountryFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Country {}'.format(n))
    area = factory.LazyAttribute(lambda o: random.randint(1000, 9999999))
    pop2005 = factory.LazyAttribute(lambda o: random.randint(1000, 999999))
    fips = factory.LazyAttribute(lambda o: uuid.uuid4().hex[:2])
    iso2 = factory.LazyAttribute(lambda o: uuid.uuid4().hex[:2])
    iso3 = factory.LazyAttribute(lambda o: uuid.uuid4().hex[:3])
    un = factory.Sequence(lambda n: n)
    region = factory.Sequence(lambda n: n)
    subregion = factory.Sequence(lambda n: n)
    lon = factory.Sequence(lambda n: n)
    lat = factory.Sequence(lambda n: n)
    mpoly = ProjectedMultiPolygon([
        ProjectedPolygon([
            ProjectedPoint(0, 0),
            ProjectedPoint(0, 1),
            ProjectedPoint(1, 0),
            ProjectedPoint(1, 1),
            ProjectedPoint(0, 0),
        ]),
    ])

    class Meta:
        model = Country


class CountryTestMixin(object):

    def setUp(self):
        self.country = CountryFactory.build()
        self.country.save()


class TestCountryManager(TestCase):

    def test_nearest_to_point_returns_nearest_country(self):
        country1 = CountryFactory.build()
        country1.save()

        country2 = CountryFactory.build()
        country2.mpoly = ProjectedMultiPolygon([
            ProjectedPolygon([
                ProjectedPoint(1000, 1000),
                ProjectedPoint(1000, 1001),
                ProjectedPoint(1001, 1000),
                ProjectedPoint(1001, 1001),
                ProjectedPoint(1000, 1000),
            ]),
        ])
        country2.save()

        point = ProjectedPoint(0, 0)
        nearest_country = Country.objects.nearest_to_point(point)
        self.assertEqual(nearest_country, country1)


class TestTileManager(CountryTestMixin, TestCase):

    def test_get_or_create_nearest_tile_rounds_coords(self):
        east = 12345
        north = 67890

        tile, created = Tile.objects.get_or_create_nearest_tile(
            east=east, north=north)
        self.assertTrue(created)
        self.assertEqual(tile.east, 12000)
        self.assertEqual(tile.north, 67000)

        tile, created = Tile.objects.get_or_create_nearest_tile(
            east=east+1, north=north+1)
        self.assertFalse(created)
        self.assertEqual(tile.east, 12000)
        self.assertEqual(tile.north, 67000)


class TestTile(CountryTestMixin, TestCase):

    def test_save_sets_polygon_and_country(self):
        tile = Tile(east=0, north=0)
        tile.save()

        mpoly = ProjectedMultiPolygon([
            ProjectedPolygon([
                ProjectedPoint(0, 0),
                ProjectedPoint(1000, 0),
                ProjectedPoint(1000, 1000),
                ProjectedPoint(0, 1000),
                ProjectedPoint(0, 0),
            ]),
        ])

        self.assertEqual(tile.east, 0)
        self.assertEqual(tile.north, 0)
        self.assertEqual(tile.mpoly, mpoly)
        self.assertEqual(tile.country, self.country)
