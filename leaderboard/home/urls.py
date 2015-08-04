from django.conf.urls import url

from leaderboard.home.views import LandingView

urlpatterns = [
    url('^$', LandingView.as_view(), name='home-landing'),
]
