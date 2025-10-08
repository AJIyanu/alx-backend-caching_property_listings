from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import Property
from .serializers import PropertySerializer


@method_decorator(cache_page(60 * 15), name='list')
class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Property model with automatic cache invalidation.
    """
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    
    def perform_create(self, serializer):
        """Clear cache when creating a property"""
        serializer.save()
        cache.clear()
    
    def perform_update(self, serializer):
        """Clear cache when updating a property"""
        serializer.save()
        cache.clear()
    
    def perform_destroy(self, instance):
        """Clear cache when deleting a property"""
        instance.delete()
        cache.clear()