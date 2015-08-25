from django.conf.urls import url

from leaderboard.contributors.views import (
    ContributionsConfigView,
    CreateContributionsView,
    LeadersView,
    LeadersCountryView,
    UpdateContributorView,
)

urlpatterns = [
    url('^config/', ContributionsConfigView.as_view(),
        name='contributions-config'),
    url('^add_stumbles/', CreateContributionsView.as_view(),
        name='contributions-create'),
    url('^contributor/update/', UpdateContributorView.as_view(),
        name='contributor-update'),
    url('^leaders/all/', LeadersView.as_view(),
        name='leaders-list'),
    url('^leaders/country/(?P<country_id>\w+)/', LeadersCountryView.as_view(),
        name='leaders-country-list'),
]
