from random import randint

from django.contrib.gis.geos import Polygon
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from backend.models import Provider, ServiceArea


# Create your tests here.


def create_initial_fake_data():
    fake = Faker('en_US')

    # initial data
    cycle_count = 15

    Provider.objects.bulk_create([Provider(first_name=fake.first_name(),
                                           last_name=fake.last_name(),
                                           username=fake.safe_email(),
                                           email=fake.safe_email(),
                                           phone='+77077545454',
                                           currency=fake.currency_code(),
                                           language='en'

                                           )
                                  for _ in range(cycle_count)], ignore_conflicts=True)

    provider_ids = Provider.objects.filter().values_list('id', flat=True)
    provider_count = len(provider_ids)
    polygon_list = list()
    for _ in range(10 * cycle_count):
        temp_cordinate = [float(i) for i in fake.local_latlng(country_code="US", coords_only=True)]
        temp_list = [temp_cordinate]
        for _ in range(4):
            temp_list.append([float(i) for i in fake.local_latlng(country_code="US", coords_only=True)])
        temp_list.append(temp_cordinate)
        polygon_list.append(Polygon(temp_list))
    ServiceArea.objects.bulk_create(
        [
            ServiceArea(
                name=fake.text(max_nb_chars=30, ext_word_list=None),
                price=randint(1, 100000),
                provider_id=provider_ids[randint(0, provider_count - 1)],
                polygon=polygon_list[i]
            )
            for i in range(10 * cycle_count)
        ], ignore_conflicts=True)


class ViewsTestCase(APITestCase):

    def setUp(self):
        create_initial_fake_data()
        fake = Faker('en_US')
        self.test_provider = Provider.objects.create(first_name=fake.first_name(),
                                                     last_name=fake.last_name(),
                                                     username=fake.safe_email(),
                                                     email=fake.safe_email(),
                                                     phone='+77077545454',
                                                     currency=fake.currency_code(),
                                                     language='en'

                                                     )
        self.test_provider.set_password('password')
        self.test_provider_key = Token.objects.create(user=self.test_provider).key

    def test_provider_service_areas_actions(self):
        c = APIClient(HTTP_AUTHORIZATION=f'Token {self.test_provider_key}')

        # check create
        data = {
            "name": "dsger",
            "price": 134,
            "polygon": [
                [102.0, 0.0],
                [103.0, 1.0],
                [104.0, 0.0],
                [105.0, 1.0],
                [102.0, 0.0]
            ]
        }

        response = c.post(reverse('backend:my-service-areas'), json.dumps(data),
                          content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['Status'])
        service_area_id = response.json()['Service area object']['id']

        # check update
        data = {
            "name": "new_name",
            "price": 234,
            "polygon": [
                [5, 5],
                [5, -5],
                [-5, 5],
                [-5, 5],
                [5, 5]
            ],
            "id": service_area_id
        }

        # check get my service areas
        response = c.put(reverse('backend:my-service-areas'), json.dumps(data),
                         content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['Status'])

        response = c.get(reverse('backend:my-service-areas'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['type'], 'FeatureCollection')

        # check search
        data = {
            'lat': 2,
            'lng': 2

        }
        response = c.get(reverse('backend:search-service-areas'), data)
        print(response.json())
        self.assertEqual(response.status_code, 200)

        # check delete
        data = {

            "id": service_area_id
        }

        response = c.delete(reverse('backend:my-service-areas'), json.dumps(data),
                            content_type="application/json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['Status'])
