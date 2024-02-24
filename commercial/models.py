from django.utils.translation import gettext_lazy as _
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """ Продукт """
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    model = models.CharField(max_length=300, verbose_name=_("Model"))
    release_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Release Date"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contacts(models.Model):
    """ Контакты """
    email = models.EmailField(verbose_name=_("Email"))
    country = models.CharField(max_length=300, verbose_name=_("Country"))
    city = models.CharField(max_length=300, verbose_name=_("City"))
    street = models.CharField(**NULLABLE, max_length=300, verbose_name=_("Street"))
    house = models.CharField(**NULLABLE, max_length=10, verbose_name=_("House"))


FACTORY = "FA"
INDIVIDUAL_ENTREPRENEUR = "IE"

# Выбор типа поставщика (Завод или индивидуальный предприниматель)
PROVIDER_TYPE_CHOICES = [
        (FACTORY, _("Factory")),
        (INDIVIDUAL_ENTREPRENEUR, _("Individual Entrepreneur")),
    ]


class BaseModel(models.Model):
    """ Базовая модель """
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    contacts = models.ForeignKey(Contacts, **NULLABLE, on_delete=models.CASCADE, verbose_name=_("Contacts"))
    arrears = models.DecimalField(**NULLABLE, max_digits=12, max_length=2, verbose_name=_("Arrears"))
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Time"))

    def __str__(self):
        return self.name


class Provider(BaseModel):
    """ Поставщик """
    provider_type = models.CharField(max_length=2, choices=PROVIDER_TYPE_CHOICES, verbose_name=_("Provider Type"))
    products = models.ManyToManyField(Product, verbose_name=_("Products"))
    provider = models.ManyToManyField(
        'self', **NULLABLE, related_name='customer', verbose_name=_("Provider")
    )

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class RetailNetwork(BaseModel):
    """ Розничная сеть """
    provider = models.ManyToManyField(
        Provider, **NULLABLE, related_name='customer', verbose_name=_("Provider")
    )

    class Meta:
        verbose_name = 'Розничная сеть'
        verbose_name_plural = 'Розничные сети'
