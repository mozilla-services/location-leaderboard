from django.conf.urls import url

from leaderboard.locations.views import ListCountriesView

urlpatterns = [
    url('^countries/', ListCountriesView.as_view(), name='countries-list'),
]
