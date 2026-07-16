from django.db import models
from airplanes.models import Airplane
from airports.models import Airport


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