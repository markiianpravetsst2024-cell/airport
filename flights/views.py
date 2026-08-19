from rest_framework import viewsets, mixins
from .models import Flight, Ticket, Order
from .serializers import FlightSerializer, TicketSerializer, FlightReadSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from airports.permissions import IsAdminOrReadOnly
from .filters import FlightFilter, TicketFilter

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = FlightFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FlightReadSerializer
        return FlightSerializer

class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user)