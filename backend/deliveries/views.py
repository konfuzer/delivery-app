from django.db.models import Avg, Count
from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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
    permission_classes = [permissions.AllowAny] #IsAuthenticated если используется токен

class PackagingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer
    permission_classes = [permissions.AllowAny] #IsAuthenticated

class DeliveryServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryService.objects.all()
    serializer_class = DeliveryServiceSerializer
    permission_classes = [permissions.AllowAny] #IsAuthenticated если используется токен

class DeliveryStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [permissions.AllowAny] #IsAuthenticated если используется токен

class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    permission_classes = [permissions.AllowAny] #IsAuthenticated если используется токен

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    permission_classes = [permissions.AllowAny] #IsAuthenticated если используется токен

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DeliveryCreateSerializer
        return DeliverySerializer


def report_dashboard(request):
    return render(request, 'reports/report_dashboard.html')

@api_view(['GET'])
@permission_classes([permissions.AllowAny]) #IsAuthenticated если используется токен
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

    grouped_by_date = deliveries.values('delivery_date').annotate(
        total=Count('id'),
        avg_distance_km=Avg('distance_km')
    ).order_by('delivery_date')

    chart_data = {
        "labels": [str(d["delivery_date"]) for d in grouped_by_date],
        "total_count": [d["total"] for d in grouped_by_date],
        "avg_distance": [float(d["avg_distance_km"]) if d["avg_distance_km"] else 0 for d in grouped_by_date],
    }

    table_data = []
    for index, d in enumerate(deliveries.select_related("transport_model", "service", "cargo_type", "status", "created_by"), start=1):
        table_data.append({
            "total": index,
            "delivery_date": str(d.delivery_date),
            "transport_model": d.transport_model.name if d.transport_model else "–",
            "packaging": d.packaging.name if d.packaging else "–",
            "service": d.service.name if d.service else "–",
            "status": d.status.status if d.status else "–",
            "cargo_type": d.cargo_type.name if d.cargo_type else "–",
            "distance_km": float(d.distance_km) if d.distance_km else 0,
            "created_by": d.created_by.username if d.created_by else "–"
        })

    return Response({
        "chart": chart_data,
        "table": table_data
    })
