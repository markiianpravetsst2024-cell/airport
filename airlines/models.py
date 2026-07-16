from django.db import models
from airports.models import Airport


class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    airports = models.ManyToManyField(Airport, related_name='airlines')

    def __str__(self):
        return self.name
