from django.conf.urls import url

from leaderboard.contributors.views import (
    UpdateContributorView,
)

urlpatterns = [
    url('^(?P<uid>\w+)/$', UpdateContributorView.as_view(),
        name='contributors-detail'),
]
