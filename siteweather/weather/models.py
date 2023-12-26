from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=255)
    # user_id = models.IntegerField()
    latitude = models.DecimalField(max_digits=10, decimal_places=4)
    longitude = models.DecimalField(max_digits=10, decimal_places=4)