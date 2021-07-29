from django.shortcuts import render  # noqa
from rest_framework import viewsets
from users.serializers import PersonSerializer, SpeciesSerializer
from .models import Person, Species, Wikis, Front_Cover

# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
   queryset = Person.objects.all()
   serializer_class = PersonSerializer


class SpeciesViewSet(viewsets.ModelViewSet):
   queryset = Species.objects.all()
   serializer_class = SpeciesSerializer
