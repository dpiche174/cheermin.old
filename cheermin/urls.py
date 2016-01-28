"""Cheermin URLs configuration."""

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, views, viewsets
from rest_framework.response import Response

from . import models
from .serializers import CoachSerializer

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Serializers define the API representation.
class AthleteSerializer(serializers.HyperlinkedModelSerializer):
    emails = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Athlete
        fields = ('id', 'first_name', 'last_name', 'phone', 'birthday', 'emails')

# ViewSets define the view behavior.
class AthleteViewSet(viewsets.ModelViewSet):
    """"""

    queryset = models.Athlete.objects.filter(teams__name='Dynastie').order_by('first_name')  # pylint: disable=E1101
    serializer_class = AthleteSerializer

class CoachesViewSet(viewsets.ModelViewSet):
    """"""

    serializer_class = CoachSerializer

    def get_queryset(self):
        return User.objects.filter(user__groups__name='Coaches').order_by('first_name')

    def retrieve(self, request, pk=None):
        pass

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'athletes', AthleteViewSet)
router.register(r'coaches', CoachesViewSet, 'coach')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'rest/api/1/',  include(router.urls)),
    url(r'rest/auth/1/', include('rest_framework.urls', namespace='rest_framework'))
]
