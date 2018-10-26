from django_filters import rest_framework as myfilters
from .models import *


class AlumnoFilter(myfilters.FilterSet):
    apellido = myfilters.CharFilter('apellido', lookup_expr='istartswith')
    strict = True

    class Meta:
        model = Alumno
        fields = ['apellido']


class ClaseFilter(myfilters.FilterSet):
    dia = myfilters.CharFilter(name='dia', lookup_expr='iexact')
    strict = True

    class Meta:
        model = Clase
        fields = ['dia']
