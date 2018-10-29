from rest_framework import viewsets
from .serializers import *
from .filters import *
from rest_framework import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def validate_args(request, arg):
    arg_name = request.query_params.get(arg)

    if request.query_params == {}:
        return 1

    if arg_name:
        return 2
    else:
        return 0

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
        # if self.kwargs.get('pk'):
        #     return Alumno.objects.all()

        if validate_args(self.request, "apellido") == 1:
            result_clase = Alumno.objects.all()
        elif validate_args(self.request, "apellido") == 2:
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

        if (validate_args(self.request, "fecha_desde") * validate_args(self.request, "fecha_hasta")) == 1:
            result_clase = Asistencia.objects.all()
        elif (validate_args(self.request, "fecha_desde") * validate_args(self.request, "fecha_hasta")) == 4:
            result_clase = Asistencia.objects.filter(fecha__range=(self.request.query_params.get("fecha_desde"), self.request.query_params.get("fecha_hasta")))
        else:
            raise exceptions.NotFound('Query mal formada o no permitida')

        return result_clase


# class ClaseDiaView(viewsets.ModelViewSet):
#     serializer_class = ClaseAlumnoSerializer
#
#     def get_queryset(self):
#
#         if validate_args(self.request, "dia") == 1:
#             result_clase = Clase.objects.all()
#         elif validate_args(self.request, "dia") == 2:
#             result_clase = Clase.objects.filter(dia__iexact=self.request.query_params.get("dia"))
#         else:
#             raise exceptions.NotFound('Query mal formada o no permitida')
#
#         return result_clase


class RegistroClasesView(viewsets.ModelViewSet):
    """
    API endpoint that allows Alumnos instances
    to be viewed or edited.
    """
    serializer_class = RegistroClasesSerializer

    def get_queryset(self):

        if validate_args(self.request, "fecha") == 1:
            result_clase = RegistroClase.objects.all()
        elif validate_args(self.request, "fecha") == 2:
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

        if (validate_args(self.request, "fecha_desde") * validate_args(self.request, "fecha_hasta")) == 1:
            result_clase = CuentaCorriente.objects.all()
        elif (validate_args(self.request, "fecha_desde") * validate_args(self.request, "fecha_hasta")) == 4:
            result_clase = CuentaCorriente.objects.filter(fecha__range=(self.request.query_params.get("fecha_desde"), self.request.query_params.get("fecha_hasta")))
        else:
            result_clase = None

        if result_clase:
            if validate_args(self.request, "concepto") == 1:
                result_clase = result_clase
            elif validate_args(self.request, "concepto") == 2:
                result_clase = result_clase.filter(concepto__iexact=(self.request.query_params.get("concepto")))
            else:
                raise exceptions.NotFound('Query mal formada o no permitida')
        else:
            raise exceptions.NotFound('Query mal formada o no permitida')

        return result_clase


def set_asistencias(request):



    response = Response({"detail": "This action is not authorized"})
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}

    return response

