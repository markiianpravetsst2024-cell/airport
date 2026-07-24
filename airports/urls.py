from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CountryListAPIView, CountryDetailAPIView, CityListAPIView, CityDetailAPIView, AirportViewSet, AirlineViewSet, AirplaneViewSet)

router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'airlines', AirlineViewSet)
router.register(r'airplanes', AirplaneViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('countries/', CountryListAPIView.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetailAPIView.as_view(), name='country-detail'),
    path('cities/', CityListAPIView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetailAPIView.as_view(), name='city-detail'),
]