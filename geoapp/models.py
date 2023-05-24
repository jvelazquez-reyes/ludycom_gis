from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GeoLocalizer(models.Model):
  latitude = models.DecimalField(max_digits=15, decimal_places=10)
  longitude = models.DecimalField(max_digits=15, decimal_places=10)
  place = models.TextField(max_length=50)
  name = models.TextField(max_length=200)
  distance = models.TextField(max_length=10)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return 'Geoapp - ' + self.user.username
