from airports.serializers import AirplaneSerializer, AirportSerializer
from django.utils import timezone
from rest_framework import serializers
from .models import Flight, Ticket, Order
from django.db import transaction

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'airplane', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'status']
        read_only_fields = ['id']

    def validate(self, data):
            departure_time = data.get('departure_time', getattr(self.instance, 'departure_time', None))
            arrival_time = data.get('arrival_time', getattr(self.instance, 'arrival_time', None))
            departure_airport = data.get('departure_airport', getattr(self.instance, 'departure_airport', None))
            arrival_airport = data.get('arrival_airport', getattr(self.instance, 'arrival_airport', None))
            if self.instance is None and departure_time and departure_time <= timezone.now():
                raise serializers.ValidationError({"departure_time": "Departure time must be in the future for a new flight."})
            if arrival_time and departure_time:
                if arrival_time <= departure_time:
                    raise serializers.ValidationError({"arrival_time":"The arrival time must be later than the departure time."})
            if  departure_airport == arrival_airport:
                        raise serializers.ValidationError({"arrival_airport": "The departure and arrival airports cannot be the same."})
            return data


class FlightReadSerializer(serializers.ModelSerializer):
    airplane = AirplaneSerializer(read_only=True)
    departure_airport = AirportSerializer(read_only=True)
    arrival_airport = AirportSerializer(read_only=True)
    class Meta:
        model = Flight
        fields =  ['id', 'flight_number', 'airplane', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'status']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'flight', 'seat_number', 'price', 'status']
        read_only_fields = ['id']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ticket price must be greater than zero.")
        return value

    def validate_status(self, value):
        if self.instance is None and value != Ticket.Status.BOOKED:
            raise serializers.ValidationError("A new ticket must be created with status 'booked'.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'created_at', 'tickets')
        read_only_fields = ('user', 'created_at')

    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
        return order