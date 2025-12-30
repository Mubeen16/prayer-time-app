from rest_framework import serializers
from users.models import User
from rafeeq.models import Subscription, Habit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'name', 'timezone', 'latitude', 'longitude']
        extra_kwargs = {'phone_number': {'validators': []}} # Handle validation manually for upsert

class OptInSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True)
    timezone = serializers.CharField(required=False, default="UTC")
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    preferences = serializers.JSONField(required=False, default=dict)

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    name = serializers.CharField()
    preferences = serializers.JSONField()
