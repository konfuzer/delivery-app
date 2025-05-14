from django.db import models
from django.contrib.auth.models import User


class TransportModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Транспортная модель"
        verbose_name_plural = "Транспортные модели"


class PackagingType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Тип упаковки"
        verbose_name_plural = "Типы упаковки"


class DeliveryService(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Услуга доставки"
        verbose_name_plural = "Услуги доставки"


class DeliveryStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status
        
    class Meta:
        verbose_name = "Статус доставки"
        verbose_name_plural = "Статусы доставки"


class CargoType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Тип груза"
        verbose_name_plural = "Типы груза"


class Delivery(models.Model):
    delivery_date = models.DateField(verbose_name="Дата доставки")
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Расстояние (км)")
    transport_model = models.ForeignKey(TransportModel, on_delete=models.SET_NULL, null=True, verbose_name="Модель транспорта")
    packaging = models.ForeignKey(PackagingType, on_delete=models.SET_NULL, null=True, verbose_name="Упаковка")
    service = models.ForeignKey(DeliveryService, on_delete=models.SET_NULL, null=True, verbose_name="Услуга")
    status = models.ForeignKey(DeliveryStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус")
    cargo_type = models.ForeignKey(CargoType, on_delete=models.SET_NULL, null=True, verbose_name="Тип груза")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создал", related_name="created_deliveries")

    def __str__(self):
        return f"{self.delivery_date} ({self.transport_model})"
        
    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"
