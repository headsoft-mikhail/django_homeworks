from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()
    image = models.TextField()
    release_date = models.DateTimeField(default=None)
    lte_exists = models.BooleanField(default=True)
    slug = models.CharField(max_length=50)


