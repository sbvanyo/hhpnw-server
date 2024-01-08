from django.db import models
from .user import User

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    open = models.BooleanField()
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
