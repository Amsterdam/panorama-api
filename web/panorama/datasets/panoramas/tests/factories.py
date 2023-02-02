import factory

from .. import models


class PanoramaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Panoramas


class TrajectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Traject
