# from rest_framework import viewsets
# from rest_framework.response import Response
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
# from django.core.cache import cache
# from .models import Property
# from .serializers import PropertySerializer


# @method_decorator(cache_page(60 * 15), name='list')
# class PropertyViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for Property model with automatic cache invalidation.
#     """
#     queryset = Property.objects.all().order_by('-created_at')
#     serializer_class = PropertySerializer
    
#     def perform_create(self, serializer):
#         """Clear cache when creating a property"""
#         serializer.save()
#         cache.clear()
    
#     def perform_update(self, serializer):
#         """Clear cache when updating a property"""
#         serializer.save()
#         cache.clear()
    
#     def perform_destroy(self, instance):
#         """Clear cache when deleting a property"""
#         instance.delete()
#         cache.clear()


from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_redis_cache_metrics

# Cache for 15 minutes (60 seconds * 15 = 900 seconds)
@cache_page(60 * 15)
def property_list(request):
    """
    View to return all properties.
    This view is cached for 15 minutes in Redis.
    """
    properties = Property.objects.all().order_by('-created_at')
    
    # Prepare data for JSON response
    properties_data = []
    for prop in properties:
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),  # Convert Decimal to string for JSON
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        })
    
    return JsonResponse({
        'count': len(properties_data),
        'properties': properties_data
    }, safe=False)

def cache_metrics(request):
    """
    View to display Redis cache metrics.
    GET /properties/metrics/
    """
    metrics = get_redis_cache_metrics()
    
    return JsonResponse({
        'status': 'success',
        'metrics': metrics,
        'description': {
            'keyspace_hits': 'Number of successful key lookups',
            'keyspace_misses': 'Number of failed key lookups',
            'hit_ratio': 'Cache efficiency (0.0 to 1.0)',
            'hit_ratio_percentage': 'Cache efficiency as percentage',
            'total_requests': 'Total cache requests',
            'cache_keys': 'Number of keys in cache',
            'used_memory': 'Memory used by Redis',
            'connected_clients': 'Number of connected clients'
        }
    })