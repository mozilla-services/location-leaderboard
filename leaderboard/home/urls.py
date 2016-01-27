from django.conf.urls import url

from leaderboard.home.views import LandingView, VersionView, HeartbeatView

urlpatterns = [
    url('^$', LandingView.as_view(), name='home-landing'),
    url('^__version__$', VersionView.as_view(), name='home-version'),
    url('^__heartbeat__$', HeartbeatView.as_view(), name='home-heartbeat'),
]
