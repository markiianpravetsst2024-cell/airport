from django.db import models
from django.conf import settings
from airports.models import Airplane, Airport


class Flight(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        BOARDING = "boarding", "Boarding"
        DEPARTED = "departed", "Departed"
        DELAYED = "delayed", "Delayed"
        CANCELLED = "cancelled", "Cancelled"

    flight_number = models.CharField(max_length=10, unique=True)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_airport = models.ForeignKey(Airport, related_name="departure_airport", on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name="arrival_airport", on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(choices=Status.choices, default=Status.SCHEDULED, max_length=10)

    def __str__(self):
        return self.flight_number

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Ticket(models.Model):
    class Status(models.TextChoices):
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        USED = 'used', 'Used'
        PAID = 'paid', 'Paid'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets", null=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.BOOKED)

    def __str__(self):
        return self.seat_number