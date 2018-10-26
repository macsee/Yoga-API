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
        return False

    #Diferenciar los tipos de errores, cuando la query esta vacia o cuando esta mal armada


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
    # queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    # filter_backends = (myfilters.DjangoFilterBackend,)
    # filter_class = AlumnoFilter

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Alumno.objects.all()

        if validate_args(self.request, "apellido"):
            if self.request.query_params.get("apellido") == "all":
                result_clase = Alumno.objects.all()
            else:
                result_clase = Alumno.objects.filter(apellido__istartswith=self.request.query_params.get("apellido"))
        else:
            raise exceptions.NotFound('Query mal formada o no permitida')

        return result_clase


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


class AsistenciasView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    # queryset = Asistencia.objects.all()
    serializer_class = AsistenciasSerializer

    def get_queryset(self):

        if validate_args(self.request, "fecha_desde") & validate_args(self.request, "fecha_hasta"):
            result_clase = Asistencia.objects.filter(fecha__range=(self.request.query_params.get("fecha_desde"), self.request.query_params.get("fecha_hasta")))
        else:
            result_clase = Asistencia.objects.all()

        return result_clase


class ClaseDiaView(viewsets.ModelViewSet):
    serializer_class = ClaseAlumnoSerializer

    def get_queryset(self):

        if validate_args(self.request, "dia"):
            if self.request.query_params.get("dia") == "all":
                result_clase = Clase.objects.all()
            else:
                result_clase = Clase.objects.filter(dia__iexact=self.request.query_params.get("dia"))
        else:
            raise exceptions.NotFound('Query mal formada o no permitida')

            # for clase in result_clase:
            #     clase.lista_alumnos = Alumno.objects.filter(clases=clase.pk)

        return result_clase


class RegistroClasesView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = RegistroClase.objects.all()
    serializer_class = RegistroClasesSerializer

    def get_queryset(self):

        if validate_args(self.request, "fecha"):
            if self.request.query_params.get("fecha") == "all":
                result_clase = RegistroClase.objects.all()
            else:
                result_clase = RegistroClase.objects.filter(fecha__iexact=self.request.query_params.get("fecha"))
        else:
            raise exceptions.NotFound('Query mal formada o no permitida')

        return result_clase


class PagosView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    queryset = Pago.objects.all()
    serializer_class = PagosSerializer


class CuentaCorrienteView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    # queryset = CuentaCorriente.objects.all()
    serializer_class = CuentaCorrienteSerializer

    def get_queryset(self):

        if validate_args(self.request, "fecha_desde") and validate_args(self.request, "fecha_hasta"):
            result_clase = CuentaCorriente.objects.filter(fecha__range=(self.request.query_params.get("fecha_desde"), self.request.query_params.get("fecha_hasta")))
        else:
            result_clase = CuentaCorriente.objects.all()

        if validate_args(self.request, "concepto"):
            result_clase = CuentaCorriente.objects.filter(concepto__iexact=(self.request.query_params.get("concepto")))

        return result_clase

