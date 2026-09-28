from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = 'placed', 'Placed'
        ACCEPTED = 'accepted', 'Accepted'
        OUT_FOR_PICKUP = 'out_for_pickup', 'Out for pickup'
        OUT_FOR_DELIVERY = 'out_for_delivery', 'Out for delivery'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    description = models.TextField(
        help_text="What should be picked up, e.g. '2 bags of rice from XYZ store'"
    )
    pickup_location = models.CharField(max_length=255, blank=True)
    delivery_address = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} — {self.customer} ({self.get_status_display()})"
