from django.db import models

# Create your models here.
from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    location_lat = models.FloatField()  # Latitude
    location_lon = models.FloatField()  # Longitude

    def __str__(self):
        return self.name
