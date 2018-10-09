from django_filters import rest_framework as myfilters
from .models import *


class AlumnoFilter(myfilters.FilterSet):
    search_name = myfilters.CharFilter(name='nombre', lookup_expr='istartswith')
    strict = True

    class Meta:
        model = Alumno
        fields = ['search_name']


class ClaseFilter(myfilters.FilterSet):
    dia = myfilters.CharFilter(name='dia', lookup_expr='iexact')
    strict = True

    class Meta:
        model = Clase
        fields = ['dia']
