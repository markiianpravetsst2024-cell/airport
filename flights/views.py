from rest_framework import viewsets
from .models import Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer, FlightReadSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FlightReadSerializer
        return FlightSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer