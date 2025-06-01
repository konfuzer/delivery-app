from rest_framework import serializers

from .models import (
    Delivery,
    DeliveryService,
    DeliveryStatus,
    CargoType,
    PackagingType,
    TransportModel
)


class TransportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportModel
        fields = ['id', 'name']

class PackagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingType
        fields = ['id', 'name']

class DeliveryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryService
        fields = ['id', 'name']

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ['id', 'status']

class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ['id', 'name']

class DeliverySerializer(serializers.ModelSerializer):
    transport_model = TransportModelSerializer()
    packaging = PackagingTypeSerializer()
    service = DeliveryServiceSerializer()
    status = DeliveryStatusSerializer()
    cargo_type = CargoTypeSerializer()

    class Meta:
        model = Delivery
        fields = [
            'id', 'delivery_date', 'distance_km',
            'transport_model', 'packaging', 'service', 'status', 'cargo_type'
        ]

class DeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            'delivery_date', 'distance_km',
            'transport_model', 'packaging', 'service', 'status', 'cargo_type'
        ]
        
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        if user and not user.is_anonymous:
            validated_data['created_by'] = user
        return super().create(validated_data)
