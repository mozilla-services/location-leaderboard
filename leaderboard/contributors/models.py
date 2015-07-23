from django.db import models


class Contributor(models.Model):
    """
    A contributor to the leaderboard.
    Synchronizes with Firefox Accounts.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

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
