from django.contrib.auth import get_user_model
from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=4)
    longitude = models.DecimalField(max_digits=10, decimal_places=4)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='locations', null=False, default=None)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локации'
        verbose_name_plural = 'Локации'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]