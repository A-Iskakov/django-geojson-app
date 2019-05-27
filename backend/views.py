from django.contrib.gis.geos import Polygon, Point, GEOSGeometry
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import ServiceArea, Provider
from backend.serializers import ServiceAreaSerializer


class RegisterAccount(APIView):

    def get(self, request, *args, **kwargs):
        test = Polygon(((0, 2), (2, 2), (2, 0), (2, -2), (0, -2), (-2, -2), (-2, 0), (-2, 2), (0, 2)))

        # ServiceArea.objects.create(name='asasdd', polygon=test, price=123, provider=Provider.objects.first())
        # point = GEOSGeometry('SRID=32140;POINT(3 3)')
        point = Point(1, 0)


        serializer = ServiceAreaSerializer(ServiceArea.objects.filter(polygon__contains=point), many=True, read_only=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(type(request.data['description']))
        print(isinstance(request.data['description'], list))
        return JsonResponse({'stat': True})