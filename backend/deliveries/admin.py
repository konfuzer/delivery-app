from django.contrib import admin
from .models import (
    TransportModel,
    PackagingType,
    DeliveryService,
    DeliveryStatus,
    CargoType,
    Delivery
)


class TransportModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)
    ordering = ('status',)


class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_date', 'transport_model', 'distance_km', 'service', 'status', 'created_by')
    list_filter = ('delivery_date', 'status', 'transport_model', 'service', 'cargo_type')
    search_fields = ('id', 'delivery_date', 'transport_model__name', 'service__name')
    date_hierarchy = 'delivery_date'
    ordering = ('-delivery_date',)
    list_per_page = 20


admin.site.register(TransportModel, TransportModelAdmin)
admin.site.register(PackagingType, PackagingTypeAdmin)
admin.site.register(DeliveryService, DeliveryServiceAdmin)
admin.site.register(DeliveryStatus, DeliveryStatusAdmin)
admin.site.register(CargoType, CargoTypeAdmin)
admin.site.register(Delivery, DeliveryAdmin)

# Настройка заголовков в админке
admin.site.site_header = "Система управления доставками"
admin.site.site_title = "Панель администратора доставок"
admin.site.index_title = "Добро пожаловать в систему управления доставками"
