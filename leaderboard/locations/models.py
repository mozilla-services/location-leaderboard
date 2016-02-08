from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.gis.db import models


class CountryQuerySet(models.query.GeoQuerySet):
    """
    A queryset for Countries which will annotate
    the number of observations made in that country.
    """

    def annotate_observations(self):
        return self.annotate(
            observations=models.Sum('contributorrank__observations'),
        ).filter(observations__gt=0)


class CountryManager(models.GeoManager):
    """
    A model manager for Countries which allows you to
    query countries which are closest to a point.
    """

    def get_queryset(self):
        return CountryQuerySet(self.model, using=self._db)

    def nearest_to_point(self, point):
        country = self.get_queryset().distance(point).order_by('distance')[:1]

        if country.exists():
            return country.get()


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
    geometry = models.MultiPolygonField(srid=settings.WGS84_SRID)

    objects = CountryManager()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @property
    def leaders_url(self):
        return reverse(
            'leaders-country-list',
            kwargs={'country_id': self.iso2},
        )
