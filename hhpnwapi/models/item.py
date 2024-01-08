from django.db import models

class Item(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
