from django.conf.urls import url

from leaderboard.home.views import LandingView, VersionView

urlpatterns = [
    url('^$', LandingView.as_view(), name='home-landing'),
    url('^__version__$', VersionView.as_view(), name='home-version'),
]
