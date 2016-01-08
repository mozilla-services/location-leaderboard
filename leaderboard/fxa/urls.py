from django.conf.urls import url

from leaderboard.fxa.views import (
    FXALoginView,
    FXAConfigView,
    FXARedirectView,
    FXARefreshView,
)

urlpatterns = [
    url('^login/', FXALoginView.as_view(),
        name='fxa-login'),
    url('^config/', FXAConfigView.as_view(),
        name='fxa-config'),
    url('^redirect/', FXARedirectView.as_view(),
        name='fxa-redirect'),
    url('^refresh/', FXARefreshView.as_view(),
        name='fxa-refresh'),
]
