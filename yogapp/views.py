from rest_framework import viewsets
from .serializers import *
from .filters import *
from rest_framework import response
from rest_framework import status
from rest_framework import exceptions


def validate_args(request, arg):
    arg_name = request.query_params.get(arg)

    if request.query_params != {} and arg_name:
        return True
    else:
        raise exceptions.NotFound('Query mal formada o no permitida')
        return False


class EspecialidadesView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer


class AlumnosView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    # filter_backends = (myfilters.DjangoFilterBackend,)
    # filter_class = AlumnoFilter

    # def get_queryset(self):
    #     nombre = self.request.query_params.get('nombre')
    #     pk = self.kwargs.get('pk')
    #     queryset = Alumno.objects.all()
    #
    #     if pk:
    #         if self.request.query_params != {}:
    #             raise exceptions.NotFound('Query mal formada o no permitida')
    #     else:
    #         if self.request.query_params != {} and nombre:
    #             queryset = queryset.filter(nombre__icontains=nombre)
    #         else:
    #             raise exceptions.NotFound('Query mal formada o no permitida')
    #
    #     return queryset


class ProfesoresView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class ClasesView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer
    # filter_backends = (myfilters.DjangoFilterBackend,)
    # filter_class = ClaseFilter

    # def get_queryset(self):
    #     dia = self.request.query_params.get('dia')
    #     pk = self.kwargs.get('pk')
    #     queryset = Clase.objects.all()
    #
    #     if pk:
    #         if self.request.query_params != {}:
    #             raise exceptions.NotFound('Query mal formada o no permitida')
    #     else:
    #         if self.request.query_params != {} and dia:
    #             queryset = queryset.filter(dia__iexact=dia)
    #         else:
    #             raise exceptions.NotFound('Query mal formada o no permitida')
    #
    #     return queryset


class RegistroAlumnosView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = RegistroAlumno.objects.all()
    serializer_class = RegistroAlumnoSerializer


class RegistroClasesView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = RegistroClase.objects.all()
    serializer_class = RegistroClaseSerializer


class ClaseDiaView(viewsets.ModelViewSet):
    serializer_class = ClaseAlumnoSerializer

    def get_queryset(self):

        if validate_args(self.request, "dia"):
            if self.request.query_params.get("dia") == "all":
                result_clase = Clase.objects.all()
            else:
                result_clase = Clase.objects.filter(dia__iexact=self.request.query_params.get("dia"))

            # for clase in result_clase:
            #     clase.lista_alumnos = Alumno.objects.filter(clases=clase.pk)

        return result_clase

