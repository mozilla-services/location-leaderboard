from django.conf.urls import url

from leaderboard.leaders.views import (
    LeadersCountryListView,
    LeadersGlobalListView,
)

urlpatterns = [
    url('^global/$',
        LeadersGlobalListView.as_view(),
        name='leaders-global-list'),
    url('^country/(?P<country_id>\w+)/$',
        LeadersCountryListView.as_view(),
        name='leaders-country-list'),
]
