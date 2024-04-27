from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import generics
from django.http import JsonResponse
from vendor.calculations import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, \
calculate_fulfillment_rate
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = {
                'on_time_delivery_rate': calculate_on_time_delivery_rate(instance),
                'quality_rating_avg': calculate_quality_rating_avg(instance),
                'average_response_time': calculate_average_response_time(instance),
                'fulfillment_rate': calculate_fulfillment_rate(instance)
            }
            return JsonResponse(data)
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)

# API endpoint to acknowledge a purchase order
@csrf_exempt
@require_POST
def acknowledge_purchase_order(request, po_id):
    try:
        po = PurchaseOrder.objects.get(pk=po_id)
        po.acknowledgment_date = timezone.now()
        po.save()
        # Recalculate average response time
        vendor = po.vendor
        vendor.average_response_time = calculate_average_response_time(vendor)
        vendor.save()
        return JsonResponse({'message': 'Purchase order acknowledged successfully'})
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase order not found'}, status=404)
    
