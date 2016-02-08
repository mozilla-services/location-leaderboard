from django.conf.urls import url

from leaderboard.contributors.views import CreateContributionsView

urlpatterns = [
    url('^$', CreateContributionsView.as_view(),
        name='contributions-create'),
]
