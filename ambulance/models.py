from django.db import models

# Create your models here.
from django.db import models

class Ambulance(models.Model):
    driver_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)
    location_lat = models.FloatField()  # Latitude
    location_lon = models.FloatField()  # Longitude
    is_available = models.BooleanField(default=True)  # For tracking availability

    def __str__(self):
        return f"{self.driver_name} - {self.vehicle_number}"
