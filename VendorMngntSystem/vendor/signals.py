from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if created or instance.status_changed:
        # Update vendor metrics based on the changes in purchase orders
        vendor = instance.vendor
        vendor.update_metrics()