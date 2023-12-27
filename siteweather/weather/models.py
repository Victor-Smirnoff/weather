from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    # user_id = models.IntegerField()
    latitude = models.DecimalField(max_digits=10, decimal_places=4)
    longitude = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локации'
        verbose_name_plural = 'Локации'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]