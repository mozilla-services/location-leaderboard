import operator

from bulk_update.helper import bulk_update
from django.db import models


class Contributor(models.Model):
    """
    A contributor to the leaderboard.
    Synchronizes with Firefox Accounts.
    """
    access_token = models.CharField(max_length=255, unique=True)
    uid = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return self.name


class ContributorRankQuerySet(models.QuerySet):
    """
    A queryset for ContributorRank objects which knows that
    when country is set to None it refers to a global rank.
    """

    def all_global(self):
        """
        Return all global ranks.
        """
        return self.filter(country=None)


class ContributorRank(models.Model):
    """
    The rank and number of observations for a contributor
    for each country they've contributed to, and globally where
    country is set to None.
    """
    # When country is None, store the global rank and observations
    country = models.ForeignKey('locations.Country', blank=True, null=True)
    contributor = models.ForeignKey(Contributor, related_name='ranks')
    observations = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)

    objects = ContributorRankQuerySet.as_manager()

    class Meta:
        unique_together = ('contributor', 'country')
        ordering = ('rank',)

    def __unicode__(self):
        return u'country: {} contributor: {} observations: {} rank: {}'.format(
            self.id,
            self.country_id,
            self.contributor_id,
            self.observations,
            self.rank,
        )

    @classmethod
    def _compute_ranks(cls, contributions):
        # Pull the entire set of ranks into memory.
        contributor_ranks = {
            (rank.contributor_id, rank.country_id): rank
            for rank in ContributorRank.objects.all()
        }

        for contribution in contributions:
            # Each contribution counts towards the rank in the country in which
            # it was made, as well as the global rank for that contributor.
            for country_id in (contribution.tile.country_id, None):
                rank_key = (contribution.contributor_id, country_id)
                contributor_rank = contributor_ranks.get(rank_key, None)

                if contributor_rank is not None:
                    # This rank exists and so we can update its observation
                    # count.
                    contributor_rank.observations += contribution.observations
                else:
                    # This contributor has no rank for that country, we should
                    # create a new one.
                    contributor_ranks[rank_key] = ContributorRank(
                        contributor_id=contribution.contributor_id,
                        country_id=country_id,
                        observations=contribution.observations,
                    )

        # Create a list of country ids from the contribution keys.
        # This saves us from needing to query the database for the country ids.
        country_ids = set([
            country_id for (contributor_id, country_id)
            in contributor_ranks.keys()
        ])

        for country_id in country_ids:
            country_ranks = sorted(
                # We have every rank for a country in memory already,
                # so we can just filter and sort this dataset.
                [
                    rank for rank in contributor_ranks.values()
                    if rank.country_id == country_id
                ],
                key=operator.attrgetter('observations'),
                reverse=True,
            )

            # Assign each contributor their new ranks for this country.
            for rank, contributor_rank in enumerate(country_ranks, start=1):
                contributor_rank.rank = rank

        # Update the ranks which already appear in the database.
        bulk_update(
            [
                rank for rank in contributor_ranks.values()
                if rank.id is not None
            ],
            update_fields=['rank', 'observations'],
            batch_size=100,
        )

        # Insert the new ranks which we created.
        ContributorRank.objects.bulk_create(
            [rank for rank in contributor_ranks.values() if rank.id is None],
        )

        # Remove the contributions which we used to calculate the new ranks.
        contribution_ids = [contribution.id for contribution in contributions]
        Contribution.objects.filter(id__in=contribution_ids).delete()

    @classmethod
    def compute_ranks(cls):
        """
        Compute the number of observations and ranks for
        each contributor for each country and globally.
        """
        # Pull all contributions into memory,  we will only work on this
        # dataset while new contributions enter the database.
        contributions = list(Contribution.objects.all().select_related('tile'))
        cls._compute_ranks(contributions)


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
        return unicode(self.date)
