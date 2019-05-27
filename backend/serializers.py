from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework.relations import StringRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from backend.models import ServiceArea


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    price = MoneyField(max_digits=14, decimal_places=2, required=True)

    class Meta:
        model = ServiceArea
        geo_field = 'polygon'
        fields = (
            'id', 'name', 'price', 'provider', 'polygon',
        )


class ServiceAreaSearchSerializer(GeoFeatureModelSerializer):
    provider = StringRelatedField()

    class Meta:
        model = ServiceArea
        geo_field = 'polygon'
        fields = (
            'id', 'name', 'price', 'provider', 'polygon',
        )
