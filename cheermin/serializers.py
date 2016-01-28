# -----------------------------------------------------------------------------
# Import
# ------
#
# - Python Standard Library

# - Other Libraries or Frameworks
from rest_framework import serializers

# - Local Application
from .models import Athlete

class CoachSerializer(serializers.ModelSerializer):

    emails = serializers.StringRelatedField(many=True)

    class Meta:
        model = Athlete
        fields = ('id', 'first_name', 'last_name', 'phone', 'birthday', 'emails')
