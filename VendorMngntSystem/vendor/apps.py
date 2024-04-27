from django.apps import AppConfig
from django.db.models.signals import post_save

class VendorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendor'
    def ready(self):
        from vendor.models import Vendor
        from vendor.signals import update_vendor_metrics
        post_save.connect(update_vendor_metrics, sender=Vendor, dispatch_uid='update_vendor_metrics')