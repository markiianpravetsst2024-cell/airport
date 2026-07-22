from rest_framework import serializers
from .models import Flight, Ticket

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'airplane', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'status']
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('arrival_time') and data.get('departure_time'):
            if data['arrival_time'] <= data['departure_time']:
                raise serializers.ValidationError({"arrival_time":"The arrival time must be later than the departure time."})

        if  data.get('departure_airport') == data.get('arrival_airport'):
            raise serializers.ValidationError({"arrival_airport": "The departure and arrival airports cannot be the same."})
        return data

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'flight', 'seat_number', 'price', 'status']
        read_only_fields = ['id']