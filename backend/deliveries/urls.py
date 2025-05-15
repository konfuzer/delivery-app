from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    TransportModelViewSet,
    PackagingTypeViewSet,
    DeliveryServiceViewSet,
    DeliveryStatusViewSet,
    CargoTypeViewSet,
    DeliveryViewSet,
    delivery_report
)


router = DefaultRouter()
router.register(r'transports', TransportModelViewSet)
router.register(r'packagings', PackagingTypeViewSet)
router.register(r'services', DeliveryServiceViewSet)
router.register(r'statuses', DeliveryStatusViewSet)
router.register(r'cargos', CargoTypeViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/data/', delivery_report, name='delivery_report'),
]
