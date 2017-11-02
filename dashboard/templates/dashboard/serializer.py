from rest_framework import serializers
from .models import Inflation

class InflationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inflation
