from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/fxa/', include('leaderboard.fxa.urls')),
    url(r'^api/v1/contributions/', include('leaderboard.contributors.urls')),
]
