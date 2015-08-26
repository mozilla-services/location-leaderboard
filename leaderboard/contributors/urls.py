from django.conf.urls import url

from leaderboard.contributors.views import (
    ContributionsConfigView,
    CreateContributionsView,
    ContributorsView,
    ContributorsCountryView,
    UpdateContributorView,
)

urlpatterns = [
    url('^config/', ContributionsConfigView.as_view(),
        name='contributions-config'),
    url('^add_stumbles/', CreateContributionsView.as_view(),
        name='contributions-create'),
    url('^contributor/update/', UpdateContributorView.as_view(),
        name='contributor-update'),
    url('^contributors/all/', ContributorsView.as_view(),
        name='contributors-list'),
    url('^contributors/country/(?P<country_id>\w+)/',
        ContributorsCountryView.as_view(),
        name='contributors-country-list'),
]
