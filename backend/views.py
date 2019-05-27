from _ctypes import ArgumentError

from django.contrib.gis.geos import Polygon, GEOSException
from django.http import JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import ServiceArea
from backend.serializers import ServiceAreaSerializer


class RegisterAccount(APIView):

    def get(self, request, *args, **kwargs):
        # check authorization
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Log in required',
                           'Details': 'Please authorize using Token in your HTTP header'}
                 },
                status=403
            )

        service_area_query = ServiceArea.objects.filter(provider_id=request.user.id)
        print(service_area_query.count())
        service_area_serializer = ServiceAreaSerializer(service_area_query, many=True, read_only=True)
        return Response(service_area_serializer.data)

    def post(self, request, *args, **kwargs):

        # check authorization
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Log in required', 'Details': 'Please authorize using Token in your HTTP header'}
                 },
                status=403
            )

        # add provider data to ServiceArea
        request.data['provider'] = request.user.id

        # check Polygon data
        try:
            request.data['polygon'] = Polygon(request.data['polygon'])
        except (ArgumentError, KeyError) as error_message:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Incorrect polygon parameter', 'Details': str(error_message)}},
                status=400
            )
        except GEOSException as error_message:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Invalid geodata in polygon parameter', 'Details': str(error_message)}},
                status=400
            )

        # validate data
        service_area_serializer = ServiceAreaSerializer(data=request.data)
        if service_area_serializer.is_valid():
            # save object and send to output
            service_area_serializer.save()
            return JsonResponse(
                {'Status': True,
                 'Message': 'Saved successfully',
                 'Service area object': service_area_serializer.data
                 },
                status=201
            )
        else:

            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Invalid JSON data', 'Details': service_area_serializer.errors}},
                status=400
            )

    def put(self, request, *args, **kwargs):

        # check authorization
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Log in required',
                           'Details': 'Please authorize using Token in your HTTP header'}
                 },
                status=403
            )

        if 'id' not in request.data:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Missing id parameter',
                           'Details': 'Please send id when updating data'}
                 },
                status=400
            )

        # check Polygon data
        if 'polygon' in request.data:
            try:
                request.data['polygon'] = Polygon(request.data['polygon'])
            except (ArgumentError) as error_message:
                return JsonResponse(
                    {'Status': False,
                     'Error': {'Tittle': 'Incorrect polygon parameter', 'Details': str(error_message)}},
                    status=400
                )
            except GEOSException as error_message:
                return JsonResponse(
                    {'Status': False,
                     'Error': {'Tittle': 'Invalid geodata in polygon parameter', 'Details': str(error_message)}},
                    status=400
                )

        service_area_query = ServiceArea.objects.filter(provider_id=request.user.id, id=request.data['id'])
        if service_area_query.exists():
            service_area_serializer = ServiceAreaSerializer(service_area_query.get(), data=request.data, partial=True)
            if service_area_serializer.is_valid():
                service_area_serializer.save()

                return JsonResponse(
                    {'Status': True,
                     'Message': 'Updated successfully',
                     'Service area object': service_area_serializer.data
                     },
                    status=201
                )
            else:
                return JsonResponse({'Status': False, 'Error': service_area_serializer.errors}, status=400)
        else:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Incorrect id parameter',
                           'Details': 'Please send correct id when updating data'}
                 },
                status=400
            )

# test = Polygon(((0, 2), (2, 2), (2, 0), (2, -2), (0, -2), (-2, -2), (-2, 0), (-2, 2), (0, 2)))
#
#        # ServiceArea.objects.create(name='asasdd', polygon=test, price=123, provider=Provider.objects.first())
#        # point = GEOSGeometry('SRID=32140;POINT(3 3)')
#        point = Point(1, 0)
#
#
#        serializer = ServiceAreaSerializer(ServiceArea.objects.filter(polygon__contains=point), many=True, read_only=True)
#        return Response(serializer.data)
