from django.contrib import admin
from .models import (
    TransportModel,
    PackagingType,
    DeliveryService,
    DeliveryStatus,
    CargoType,
    Delivery
)

@admin.register(TransportModel)
class TransportModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(PackagingType)
class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)
    ordering = ('status',)

@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_date', 'transport_model', 'distance_km', 'service', 'status', 'created_by')
    list_filter = ('delivery_date', 'status', 'transport_model', 'service', 'cargo_type')
    search_fields = ('id', 'delivery_date', 'transport_model__name', 'service__name')
    date_hierarchy = 'delivery_date'
    ordering = ('-delivery_date',)
    list_per_page = 20