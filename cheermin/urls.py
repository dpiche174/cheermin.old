"""Cheermin URLs configuration."""

# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other Libraries or Frameworks
from django.conf.urls import url

# - Local application
from . import views

app_name = 'cheermin'
urlpatterns = [
    url(r'^$',                                    views.index),
    url(r'^athletes/$',                           views.athletes),
    url(r'^athletes/(?P<athlete_id>\d+)/$',       views.athlete_detail),
    url(r'^athletes/(?P<athlete_id>\d+)/print/$', views.athlete_print),
    url(r'^inscriptions/photos/$',                views.photos),
]
