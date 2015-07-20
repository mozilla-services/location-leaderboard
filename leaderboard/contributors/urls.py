from django.conf.urls import url

from leaderboard.contributors.views import CreateContributionsView

urlpatterns = [
    url('^add_stumbles/', CreateContributionsView.as_view(),
        name='contributions-create'),
]
