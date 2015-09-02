from django.conf.urls import url

from leaderboard.contributors.views import (
    ContributionsConfigView,
    CreateContributionsView,
)

urlpatterns = [
    url('^config/$', ContributionsConfigView.as_view(),
        name='contributions-config'),
    url('^/$', CreateContributionsView.as_view(),
        name='contributions-create'),
]
