from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'price', 'location', 'created_at']
        read_only_fields = ['id', 'created_at']