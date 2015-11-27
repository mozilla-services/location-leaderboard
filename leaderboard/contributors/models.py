from bulk_update.helper import bulk_update
from django.db import models

from leaderboard.locations.models import Country


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
        ).filter(observations__gt=0).order_by('-observations')


class Contributor(models.Model):
    """
    A contributor to the leaderboard.
    Synchronizes with Firefox Accounts.
    """
    access_token = models.CharField(max_length=255, unique=True)
    uid = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')

    objects = ContributorQuerySet.as_manager()

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
        return unicode(self.id)

    @staticmethod
    def compute_ranks():
        """
        Compute the number of observations and ranks for
        each contributor for each country and globally.
        """
        # When country is None, compute the global ranks
        countries = [None] + list(Country.objects.all())

        contributor_ranks = {
            (rank.contributor_id, rank.country_id): rank
            for rank in ContributorRank.objects.all()
        }

        new_contributor_ranks = []
        updated_contributor_ranks = []

        for country in countries:
            contributors = Contributor.objects.all()

            if country:
                contributors = contributors.filter_country(country.iso2)

            ranked_contributors = enumerate(
                contributors.annotate_observations(), start=1)

            for rank, contributor in ranked_contributors:

                country_id = country.id if country else None
                contributor_rank = contributor_ranks.get(
                    (contributor.id, country_id), None)

                if contributor_rank:
                    contributor_rank.rank = rank
                    contributor_rank.observations = contributor.observations
                    updated_contributor_ranks.append(contributor_rank)
                else:
                    new_contributor_ranks.append(ContributorRank(
                        contributor=contributor,
                        country=country,
                        rank=rank,
                        observations=contributor.observations,
                    ))

        bulk_update(
            updated_contributor_ranks,
            update_fields=['rank', 'observations'],
            batch_size=100,
        )
        ContributorRank.objects.bulk_create(new_contributor_ranks)


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
        return u'{user}-{date}-{tile}: {observations}'.format(
            user=self.contributor,
            date=self.date,
            tile=self.tile,
            observations=self.observations,
        )
