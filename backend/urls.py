from django.urls import path

from .views import ServiceAreaView, ServiceAreaSearch

app_name = 'backend'
urlpatterns = [
    path('my-service-areas/', ServiceAreaView.as_view(), name='my-service-areas'),
    path('search-service-areas/', ServiceAreaSearch.as_view(), name='search-service-areas'),

]