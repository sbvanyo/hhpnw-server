from django.db import models
from django.utils import timezone
from .order import Order

class Revenue(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    payment = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)
    tip = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    