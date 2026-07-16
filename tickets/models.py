from django.db import models
from django.conf import settings
from flights.models import Flight

class Ticket(models.Model):
    class Status(models.TextChoices):

        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        USED = 'used', 'Used'
        PAID = 'paid', 'Paid'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.BOOKED)

    def __str__(self):
        return self.seat_number