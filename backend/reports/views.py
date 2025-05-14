from django.db.models import Count
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from deliveries.models import Delivery


def report_dashboard(request):
    return render(request, 'reports/report_dashboard.html')

@api_view(['GET'])
@permission_classes([AllowAny])
def delivery_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    service = request.GET.get('service')
    cargo = request.GET.get('cargo')

    deliveries = Delivery.objects.all()

    if start_date:
        deliveries = deliveries.filter(delivery_date__gte=start_date)
    if end_date:
        deliveries = deliveries.filter(delivery_date__lte=end_date)
    if service:
        deliveries = deliveries.filter(service__id=service)
    if cargo:
        deliveries = deliveries.filter(cargo_type__id=cargo)

    # Группировка по дате
    grouped = deliveries.values('delivery_date').annotate(total=Count('id')).order_by('delivery_date')
    chart_data = {
        "labels": [str(d["delivery_date"]) for d in grouped],
        "values": [d["total"] for d in grouped],
    }

    # Табличные данные
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
        for d in deliveries.select_related("transport_model", "service", "cargo_type", "status")
    ]

    return Response({
        "chart": chart_data,
        "table": table_data
    })