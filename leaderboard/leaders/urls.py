from django.conf.urls import url

from leaderboard.leaders.views import (
    LeaderProfileView,
    LeadersCountryListView,
    LeadersGlobalListView,
)

urlpatterns = [
    url('^profile/(?P<uid>\w+)/$',
        LeaderProfileView.as_view(),
        name='leaders-profile'),
    url('^global/$',
        LeadersGlobalListView.as_view(),
        name='leaders-global-list'),
    url('^country/(?P<country_id>\w+)/$',
        LeadersCountryListView.as_view(),
        name='leaders-country-list'),
]
