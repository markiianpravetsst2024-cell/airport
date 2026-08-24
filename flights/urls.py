from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, TicketViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]