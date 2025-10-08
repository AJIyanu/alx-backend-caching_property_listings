# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# # Create a router and register our viewset
# router = DefaultRouter()
# router.register(r'', views.PropertyViewSet, basename='property')

# app_name = 'properties'

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('metrics/', views.cache_metrics, name='cache_metrics'),
]