from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from djmoney.models.fields import CurrencyField, MoneyField
from languages.fields import LanguageField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.



class Provider(AbstractUser):

    phone = PhoneNumberField(verbose_name='Phone Number', blank=True, null=True)
    language = LanguageField(default='en')
    currency = CurrencyField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ServiceArea(models.Model):
    name = models.CharField(max_length=30)
    price = MoneyField(max_digits=14, decimal_places=2, currency_field_name='provider.currency', null=False,
                       blank=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='service_areas')
    polygon = models.PolygonField()

    def __str__(self):
        return f'{self.name} {self.price}'
