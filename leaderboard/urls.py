from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/fxa/', include('leaderboard.fxa.urls')),
    url(r'^api/v1/contributions/',
        include('leaderboard.contributors.urls')),
    url(r'^api/v1/leaders/', include('leaderboard.leaders.urls')),
    url(r'^api/v1/locations/', include('leaderboard.locations.urls')),
    url(r'^', include('leaderboard.home.urls')),
]
