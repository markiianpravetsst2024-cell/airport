from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Country, Airport, Airline, Airplane, City
from .serializers import CountrySerializer, AirportSerializer, AirlineSerializer, AirplaneSerializer, CitySerializer, AirportReadSerializer
from .permissions import IsAdminOrReadOnly
from .filters import AirportFilter, AirlineFilter, AirplaneFilter

class CountryListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountryDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Country, pk=pk)

    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def put(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        country = self.get_object(pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CityDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(City, pk=pk)

    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def put(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        city = self.get_object(pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = AirportFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AirportReadSerializer
        return AirportSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = AirlineFilter

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = AirplaneFilter

