from django.db import models


class ContributorQuerySet(models.QuerySet):
    """
    A queryset for Contributors with additional
    support for country filtering and observation
    annotation.
    """

    def filter_country(self, country_code):
        """
        Filter for contributors within the country
        defined by the provided ISO2 country code.
        """
        return self.filter(
            contribution__tile__country__iso2=country_code)

    def annotate_observations(self):
        """
        Add an 'observations' field to the contributor
        objects which counts the number of contributions
        made by the contributor, and sort by the
        greatest contributors first.
        """
        return self.annotate(
            observations=models.Sum('contribution__observations')
        ).order_by('-observations')


class Contributor(models.Model):
    """
    A contributor to the leaderboard.
    Synchronizes with Firefox Accounts.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    objects = ContributorQuerySet.as_manager()

    def __unicode__(self):
        return self.name


class Contribution(models.Model):
    """
    A contribution made by a contributor to the leaderboard.
    """
    date = models.DateField()
    tile = models.ForeignKey('locations.Tile')
    contributor = models.ForeignKey(Contributor)
    observations = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'tile', 'contributor')

    def __unicode__(self):
        return '{user}-{date}-{tile}: {observations}'.format(
            user=self.contributor,
            date=self.date,
            tile=self.tile,
            observations=self.observations,
        )
