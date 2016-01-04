from django.conf.urls import url

from leaderboard.fxa.views import FXAConfigView, FXARedirectView

urlpatterns = [
    url('^config/', FXAConfigView.as_view(),
        name='fxa-config'),
    url('^redirect/', FXARedirectView.as_view(),
        name='fxa-redirect'),
]
