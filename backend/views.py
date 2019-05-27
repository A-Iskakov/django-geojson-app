from _ctypes import ArgumentError

from django.contrib.gis.geos import Polygon, GEOSException, Point
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import ServiceArea
from backend.serializers import ServiceAreaSerializer, ServiceAreaSearchSerializer


# to perform action on service areas
class ServiceAreaView(APIView):

    # get my service areas
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
        service_area_serializer = ServiceAreaSerializer(service_area_query, many=True, read_only=True)
        return Response(service_area_serializer.data)

    # post new data
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

    # update my service area data
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

        # require id for update
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

        # validate serializer
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


class ServiceAreaSearch(APIView):

    # take a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng
    def get(self, request, *args, **kwargs):

        # lat and lng
        if {'lat', 'lng'}.issubset(request.GET):
            # convert to Point
            try:
                point = Point(float(request.GET['lat']), float(request.GET['lng']))
            except ValueError as error_message:
                return JsonResponse(
                    {'Status': False,
                     'Error': {'Tittle': 'Incorrect GET parameter', 'Details': str(error_message)}},
                    status=400
                )
            # creating query with select related for provider name
            service_area_query = ServiceArea.objects.filter(polygon__contains=point).select_related('provider')
            serializer = ServiceAreaSearchSerializer(service_area_query, many=True,
                                                     read_only=True)
            return Response(serializer.data)

        else:
            return JsonResponse(
                {'Status': False,
                 'Error': {'Tittle': 'Missing parameter(s)',
                           'Details': 'Please send lat and lng when searching polygons'}
                 },
                status=400
            )
