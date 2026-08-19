import django_filters
from .models import Flight, Ticket

class FlightFilter(django_filters.FilterSet):
    departure_after = django_filters.DateTimeFilter(field_name='departure_time', lookup_expr='gte')
    departure_before = django_filters.DateTimeFilter(field_name='departure_time', lookup_expr='lte')

    class Meta:
        model = Flight
        fields = ['status', 'departure_airport', 'arrival_airport']

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = ['status', 'flight',]
