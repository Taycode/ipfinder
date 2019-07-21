from django.db import models


class IPAddress(models.Model):
    address = models.GenericIPAddressField()
    continent = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.address
