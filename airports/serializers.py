from rest_framework import serializers
from .models import Country, Airport, Airline, Airplane, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("The city name must contain at least 2 characters.")
        return value.title()

    def validate_code(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("The city code must consist of letters only.")
        return value.upper()

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("The country name must contain at least 3 characters.")
        return value.title()

    def validate_code(self, value):
        if len(value) > 3 or not value.isalpha():
            raise serializers.ValidationError("The country code must consist of up to 3 letters (e.g., UKR or UA).")
        return value.upper()

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'country', 'city']
        read_only_fields = ['id']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("The airport name must contain at least 3 characters.")
        return value.title()

    def validate_code(self, value):
        if len(value) != 3 or not value.isalpha():
            raise serializers.ValidationError("The airport code must consist of exactly three letters.")
        return value.upper()

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'name', 'code','airport']
        read_only_fields = ['id']

class  AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'model', 'capacity', 'airline']
        read_only_fields = ['id']