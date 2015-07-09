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
    created = models.DateTimeField(auto_now_add=True)
    contributor = models.ForeignKey(Contributor)
    tile = models.ForeignKey('locations.Tile')
    observations = models.PositiveIntegerField()

    def __unicode__(self):
        return '{user}-{date}-{tile}: {observations}'.format(
            user=self.contributor,
            date=self.created,
            tile=self.tile,
            observations=self.observations,
        )
