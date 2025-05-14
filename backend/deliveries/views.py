from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Delivery, TransportModel, PackagingType, DeliveryService, DeliveryStatus, CargoType
from .serializers import (
    TransportModelSerializer,
    PackagingTypeSerializer,
    DeliveryServiceSerializer,
    DeliveryStatusSerializer,
    CargoTypeSerializer,
    DeliverySerializer,
    DeliveryCreateSerializer
)

# === API ViewSets ===
class TransportModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TransportModel.objects.all()
    serializer_class = TransportModelSerializer
    permission_classes = [permissions.AllowAny]

class PackagingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer
    permission_classes = [permissions.AllowAny]

class DeliveryServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryService.objects.all()
    serializer_class = DeliveryServiceSerializer
    permission_classes = [permissions.AllowAny]

class DeliveryStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [permissions.AllowAny]

class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    permission_classes = [permissions.AllowAny]

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DeliveryCreateSerializer
        return DeliverySerializer


def report_dashboard(request):
    return render(request, 'reports/report_dashboard.html')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def delivery_report(request):
    deliveries = Delivery.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    service_id = request.GET.get('service')
    cargo_id = request.GET.get('cargo')

    if start_date:
        deliveries = deliveries.filter(delivery_date__gte=start_date)
    if end_date:
        deliveries = deliveries.filter(delivery_date__lte=end_date)
    if service_id:
        deliveries = deliveries.filter(service_id=service_id)
    if cargo_id:
        deliveries = deliveries.filter(cargo_type_id=cargo_id)

    grouped = deliveries.values('delivery_date').annotate(total=Count('id')).order_by('delivery_date')
    chart_data = {
        "labels": [str(d["delivery_date"]) for d in grouped],
        "values": [d["total"] for d in grouped],
    }

    table_data = [
        {
            "total": 1,
            "delivery_date": str(d.delivery_date),
            "transport_model": d.transport_model.name if d.transport_model else "–",
            "service": d.service.name if d.service else "–",
            "cargo_type": d.cargo_type.name if d.cargo_type else "–",
            "status": d.status.status if d.status else "–",
            "distance": float(d.distance_km) if d.distance_km else 0,
        }
        for d in deliveries.select_related(
            "transport_model", "service", "cargo_type", "status"
        )
    ]

    return Response({
        "chart": chart_data,
        "table": table_data
    })