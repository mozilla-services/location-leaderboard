from django.conf.urls import url

from leaderboard.fxa.views import FXARedirectView

urlpatterns = [
    url('^redirect/', FXARedirectView.as_view(),
        name='fxa-redirect'),
]
