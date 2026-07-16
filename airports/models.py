from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="airports")

    def __str__(self):
        return self.name