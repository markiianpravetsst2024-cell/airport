from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, default="")

    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="airports")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='airports',null=True)

    def __str__(self):
        return self.name

class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    airports = models.ManyToManyField(Airport, related_name='airlines')

    def __str__(self):
        return self.name

class Airplane(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')

    def __str__(self):
        return self.model