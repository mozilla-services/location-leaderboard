from django.conf import settings
from django.contrib.gis.db import models

from leaderboard.locations.projected_geos import (
    ProjectedPoint,
    ProjectedPolygon,
    ProjectedMultiPolygon,
)


class CountryManager(models.GeoManager):
    """
    A model manager for Countries which allows you to
    query countries which are closest to a point.
    """

    def nearest_to_point(self, point):
        country = self.get_queryset().distance(point).order_by('distance')[:1]

        if country.exists():
            return country.get()


# Create your models here.
class Country(models.Model):
    """
    A country as defined by:
    https://docs.djangoproject.com/en/1.8/ref/contrib/gis/
    tutorial/#defining-a-geographic-model
    """

    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2, unique=True)
    iso3 = models.CharField('3 Digit ISO', max_length=3, unique=True)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()
    mpoly = models.MultiPolygonField(srid=settings.PROJECTION_SRID)

    objects = CountryManager()

    def __unicode__(self):
        return self.name


class TileManager(models.GeoManager):
    """
    A model manager for Tiles which allows you to
    query a Tile nearest to a point provided in east/north
    projected coordinates.
    """

    def get_or_create_nearest_tile(self, east=None, north=None,
                                   *args, **kwargs):
        # Round to the nearest tile size
        east = east - (east % self.model.TILE_SIZE)
        north = north - (north % self.model.TILE_SIZE)

        return self.get_or_create(*args, east=east, north=north, **kwargs)


class Tile(models.Model):
    """
    A 1km x 1km tile using the Spatial Reference System EPSG 3857
    (WGS84 Web Mercator) projection system.
    """

    # Each side of a tile is 1000m
    TILE_SIZE = 1000

    # The bottom left coordinates
    east = models.IntegerField()
    north = models.IntegerField()

    country = models.ForeignKey(Country, related_name='tiles')
    mpoly = models.MultiPolygonField(srid=settings.PROJECTION_SRID)

    objects = TileManager()

    def __unicode__(self):
        return '{east},{north}'.format(north=self.north, east=self.east)

    def save(self, *args, **kwargs):
        # If we are saving a new tile, we want to automatically
        # populate the country and geometry fields
        if not self.pk:
            # Create a box starting with the coordinates provided
            # at the bottom left
            points = [
                ProjectedPoint(self.east, self.north),
                ProjectedPoint(self.east + self.TILE_SIZE, self.north),
                ProjectedPoint(
                    self.east + self.TILE_SIZE,
                    self.north + self.TILE_SIZE,
                ),
                ProjectedPoint(self.east, self.north + self.TILE_SIZE),
                ProjectedPoint(self.east, self.north),
            ]

            self.mpoly = ProjectedMultiPolygon([ProjectedPolygon(points)])
            self.country = Country.objects.nearest_to_point(
                self.mpoly.centroid)

        return super(Tile, self).save(*args, **kwargs)
