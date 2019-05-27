from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from backend.models import ServiceArea


class ServiceAreaSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ServiceArea
        geo_field = 'polygon'
        fields = (
            'id', 'name', 'price', 'provider', 'polygon',
        )
