import django_filters
from .models import Airport, Airline, Airplane, Country, City

class AirportFilter(django_filters.FilterSet):
    class Meta:
        model = Airport
        fields = ['country', 'city']


class AirlineFilter(django_filters.FilterSet):
    class Meta:
        model = Airline
        fields = ['code']


class AirplaneFilter(django_filters.FilterSet):
    min_capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    max_capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='lte')
    class Meta:
        model = Airplane
        fields = ['airline']



class CityFilter(django_filters.FilterSet):
    class Meta:
        model = City
        fields = {
            'name': ['icontains'],
            'code': ['icontains', 'exact'],
        }

class CountryFilter(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = {
            'name': ['icontains'],
            'code': ['exact'],
        }

