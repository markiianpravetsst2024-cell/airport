from django.db import models
from airlines.models import Airline



class Airplane(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')

    def __str__(self):
        return self.model