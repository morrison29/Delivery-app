from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user so we can tell customers and the delivery guy apart.
    is_delivery_agent = True  -> this is the person doing deliveries
    is_delivery_agent = False -> this is a customer placing orders
    """
    is_delivery_agent = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        role = "Delivery Agent" if self.is_delivery_agent else "Customer"
        return f"{self.username} ({role})"
