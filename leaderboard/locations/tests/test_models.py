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
    fips = factory.Sequence(lambda n: str(n))
    iso2 = factory.Sequence(lambda n: str(n))
    iso3 = factory.Sequence(lambda n: str(n))
    un = factory.Sequence(lambda n: n)
    region = factory.Sequence(lambda n: n)
    subregion = factory.Sequence(lambda n: n)
    lon = factory.Sequence(lambda n: n)
    lat = factory.Sequence(lambda n: n)
    geometry = factory.Sequence(lambda n: ProjectedMultiPolygon([
        ProjectedPolygon([
            ProjectedPoint(n, n),
            ProjectedPoint(n, n+1),
            ProjectedPoint(n+1, n),
            ProjectedPoint(n+1, n+1),
            ProjectedPoint(n, n),
        ]),
    ]))

    class Meta:
        model = Country


class TileFactory(factory.DjangoModelFactory):
    easting = factory.Sequence(lambda n: n)
    northing = factory.Sequence(lambda n: n)
    country = factory.SubFactory(CountryFactory)
    geometry = factory.Sequence(lambda n: ProjectedMultiPolygon([
        ProjectedPolygon([
            ProjectedPoint(n, n),
            ProjectedPoint(n, n+1),
            ProjectedPoint(n+1, n),
            ProjectedPoint(n+1, n+1),
            ProjectedPoint(n, n),
        ]),
    ]))

    class Meta:
        model = Tile


class TestCountryManager(TestCase):

    def test_nearest_to_point_returns_nearest_country(self):
        country1 = CountryFactory.build()
        country1.save()

        country2 = CountryFactory.build()
        country2.geometry = ProjectedMultiPolygon([
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


class TestTileManager(TestCase):

    def setUp(self):
        self.country = CountryFactory()

    def test_get_or_create_nearest_tile_rounds_coords(self):
        easting = 12345
        northing = 67890

        tile, created = Tile.objects.get_or_create_nearest_tile(
            easting=easting, northing=northing)
        self.assertTrue(created)
        self.assertEqual(tile.easting, 12000)
        self.assertEqual(tile.northing, 67000)

        tile, created = Tile.objects.get_or_create_nearest_tile(
            easting=easting+1, northing=northing+1)
        self.assertFalse(created)
        self.assertEqual(tile.easting, 12000)
        self.assertEqual(tile.northing, 67000)


class TestTile(TestCase):

    def setUp(self):
        self.country = CountryFactory()

    def test_save_sets_polygon_and_country(self):
        tile = Tile(easting=0, northing=0)
        tile.save()

        geometry = ProjectedMultiPolygon([
            ProjectedPolygon([
                ProjectedPoint(0, 0),
                ProjectedPoint(1000, 0),
                ProjectedPoint(1000, 1000),
                ProjectedPoint(0, 1000),
                ProjectedPoint(0, 0),
            ]),
        ])

        self.assertEqual(tile.easting, 0)
        self.assertEqual(tile.northing, 0)
        self.assertEqual(tile.geometry, geometry)
        self.assertEqual(tile.country, self.country)
