from django.urls import path

from .views import ServiceAreaView, ServiceAreaSearch

app_name = 'backend'
urlpatterns = [
    path('geo/my-service-areas/', ServiceAreaView.as_view(), name='my-service-areas'),
    path('geo/search-service-areas/', ServiceAreaSearch.as_view(), name='search-service-areas'),

]