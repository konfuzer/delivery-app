from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import (
    TransportModel, PackagingType, DeliveryService,
    DeliveryStatus, CargoType, Delivery
)
from .serializers import (
    TransportModelSerializer, PackagingTypeSerializer, DeliveryServiceSerializer,
    DeliveryStatusSerializer, CargoTypeSerializer,
    DeliverySerializer, DeliveryCreateSerializer
)
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class TransportModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TransportModel.objects.all()
    serializer_class = TransportModelSerializer
    permission_classes = [AllowAny]


class PackagingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer
    permission_classes = [AllowAny]


class DeliveryServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryService.objects.all()
    serializer_class = DeliveryServiceSerializer
    permission_classes = [AllowAny]


class DeliveryStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [AllowAny]


class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer
    permission_classes = [AllowAny]


class DeliveryViewSet(viewsets.ModelViewSet):    
    queryset = Delivery.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DeliveryCreateSerializer
        return DeliverySerializer


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['detail'] = response.data.get('detail', str(exc))
    else:
        return Response({'detail': 'Internal server error', 'status_code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
