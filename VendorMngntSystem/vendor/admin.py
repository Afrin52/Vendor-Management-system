from django.contrib import admin

# Register your models here.
from vendor.models import Vendor, PurchaseOrder

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)