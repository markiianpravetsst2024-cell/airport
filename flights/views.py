from rest_framework import viewsets
from .models import Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer, FlightReadSerializer
from .permissions import IsOwnerOrAdmin, IsFlightNotDeparted
from rest_framework.permissions import IsAuthenticated
from airports.permissions import IsAdminOrReadOnly
from .filters import FlightFilter

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = FlightFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FlightReadSerializer
        return FlightSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin, IsFlightNotDeparted]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)