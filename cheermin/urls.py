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
    url(r'^$',                                 views.index),
    url(r'^athletes/$',                        views.athletes, name='athletes'),
    url(r'^athletes/(?P<athlete_id>\d+)/$',    views.athlete_detail, name='athlete_detail'),
    url(r'^inscriptions/photos/$',             views.photos),
]
