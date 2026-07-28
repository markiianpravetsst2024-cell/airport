import re
from rest_framework import serializers
from .models import Country, Airport, Airline, Airplane, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("The city name must contain at least 2 characters.")
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("The city name cannot contain numbers.")
        return value.title()

    def validate_code(self, value):
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z]{2,4}', value):
            raise serializers.ValidationError("The city code must consist of letters only.")
        return value

class CountrySerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("The country name must contain at least 3 characters.")
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("The country name cannot contain numbers.")
        return value.title()

    def validate_code(self, value):
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z]{1,3}', value):
            raise serializers.ValidationError("The country code must consist of up to 3 letters (e.g., UKR or UA).")
        return value

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'country', 'city']
        read_only_fields = ['id']

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("The airport name must contain at least 3 characters.")
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("The airport name cannot contain numbers.")
        return value.title()

    def validate_code(self, value):
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z]{3}', value):
            raise serializers.ValidationError("The airport code must consist of exactly three letters.")
        return value

class AirportReadSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'country', 'city']

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'name', 'code','airports']
        read_only_fields = ['id']

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("The airline name must contain at least 2 characters.")
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("The airline name cannot contain numbers.")
        return value.title()

    def validate_code(self, value):
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z0-9]{2,3}', value):
            raise serializers.ValidationError("Airline code must be 2-3 letters/digits (e.g., PS, S7).")
        return value

class  AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'model', 'capacity', 'airline']
        read_only_fields = ['id']

    def validate_model(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Airplane model name is too short.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Airplane model name must contain at least one letter.")
        return value

    def validate_capacity(self, value):
        if value == 0:
            raise serializers.ValidationError("Airplane capacity must be greater than zero.")
        if value > 900:
            raise serializers.ValidationError("Aircraft capacity maximum of approximately 900 seats.")
        return value

