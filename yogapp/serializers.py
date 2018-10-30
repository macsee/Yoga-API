from rest_framework import serializers
from .models import *
import datetime
from datetime import date, timedelta


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ('url', 'pk', 'nombre', 'descripcion')


class AlumnoSerializer(serializers.ModelSerializer):
    # registro = serializers.StringRelatedField(many=True)

    class Meta:
        model = Alumno
        fields = '__all__'


class ProfesorSerializer(serializers.ModelSerializer):
    # clases = ClaseSerializer(many=True, read_only=False)

    class Meta:
        model = Profesor
        fields = '__all__'
        # fields = ('url', 'pk', 'nombre', 'apellido', 'especialidad', 'dni', 'tel', 'fecha_nac')


class PagosSerializer(serializers.ModelSerializer):
    # clases = ClaseSerializer(many=True, read_only=False)

    class Meta:
        model = Pago
        fields = '__all__'


class AsistenciasSerializer(serializers.ModelSerializer):
    # clases = ClaseSerializer(many=True, read_only=False)

    class Meta:
        model = Asistencia
        fields = '__all__'


class ClaseSerializer(serializers.ModelSerializer):
    profesor_ = serializers.SerializerMethodField(method_name='get_profesor_data')
    hora_inicio = serializers.TimeField(format="%H:%M")
    hora_fin = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Clase
        # depth = 1
        fields = ('id', 'nombre', 'profesor', 'profesor_', 'dia', 'hora_inicio', 'hora_fin', 'cupo')

    @staticmethod
    def get_profesor_data(obj):
        if obj.profesor is None:
            return {}
        else:
            return {
                    'nombre': obj.profesor.nombre,
                    'apellido': obj.profesor.apellido,
                    'id': obj.profesor.id
                    }


class RegistroClasesSerializer(serializers.ModelSerializer):

    lista_alumnos = serializers.SerializerMethodField(method_name='get_lista_alumno')
    profesor_ = serializers.SerializerMethodField(method_name='get_profesor_data')
    hora_inicio = serializers.TimeField(format="%H:%M")
    hora_fin = serializers.TimeField(format="%H:%M")

    class Meta:
        model = RegistroClase
        fields = ('id', 'nombre', 'clase_orig', 'lista_alumnos', 'profesor_', 'fecha', 'hora_inicio', 'hora_fin', 'estado', 'cupo')

    @staticmethod
    def get_lista_alumno(obj):
        lista_alumnos = []
        now = datetime.datetime.now() - datetime.timedelta(hours=3)

        if now.date() > obj.fecha: #Pasado
            alumno = Asistencia.objects.filter(clase_registro=obj.id)
            for al in alumno:
                lista_alumnos.append(
                    {
                        'nombre': '%s, %s' % (al.alumno.apellido, al.alumno.nombre),
                        'alumno_pk': al.alumno.id,
                        'asist_pk': al.id,
                    }
                )
        elif now.date() < obj.fecha: #Futuro
            alumno = Alumno.objects.filter(clases=obj.clase_orig)
            for al in alumno:
                if al.activo:
                    lista_alumnos.append(
                        {
                            'nombre': '%s, %s' % (al.apellido, al.nombre),
                            'alumno_pk': al.id,
                            'asist_pk': None,
                        }
                    )
        else: #Presente. Hay que combinar los alumnos de la clase mas los que ya tienen asistencia
            alumnos_presentes = Asistencia.objects.filter(clase_registro_id=obj.id)
            alumnos_clase = Alumno.objects.filter(clases=obj.clase_orig)

            for al in alumnos_presentes:
                lista_alumnos.append(
                    {
                        'nombre': '%s, %s' % (al.alumno.apellido, al.alumno.nombre),
                        'alumno_pk': al.alumno.id,
                        'asist_pk': al.id,
                    }
                )

            li = [x['alumno_pk'] for x in lista_alumnos]

            for al in alumnos_clase:
                if al.id not in li:
                    lista_alumnos.append(
                        {
                            'nombre': '%s, %s' % (al.apellido, al.nombre),
                            'alumno_pk': al.id,
                            'asist_pk': None,
                        }
                    )

        return lista_alumnos

    @staticmethod
    def get_profesor_data(obj):
        
        if obj.profesor is None:
            return {}
        else:    
            return {
                'nombre': '%s, %s' % (obj.profesor.apellido, obj.profesor.nombre),
                'id': obj.profesor.id
            }


# class ClaseAlumnoSerializer(serializers.ModelSerializer):
#     # clase = serializers.SerializerMethodField(method_name='get_clase_data')
#     # alumno = serializers.SerializerMethodField(method_name='get_alumno_data')
#     lista_alumnos = serializers.SerializerMethodField(method_name='get_lista_alumno')
#     profesor = serializers.SerializerMethodField(method_name='get_profesor_data')
#     hora_inicio = serializers.TimeField(format="%H:%M")
#     hora_fin = serializers.TimeField(format="%H:%M")
#
#     class Meta:
#         model = Clase
#         fields = ('id', 'nombre', 'lista_alumnos', 'profesor', 'dia', 'hora_inicio', 'hora_fin')
#         # fields = ('pk', 'alumno', 'clase')
#
#     @staticmethod
#     def get_lista_alumno(obj):
#         lista_alumnos = []
#         alumno = Alumno.objects.filter(clases=obj.id)
#         for al in alumno:
#             lista_alumnos.append(
#                 {
#                     'nombre': '%s, %s' % (al.apellido, al.nombre),
#                     'id': al.id
#                 }
#             )
#
#         return lista_alumnos
#
#     @staticmethod
#     def get_profesor_data(obj):
#         if obj.profesor is None:
#             return None
#         else:
#             return {
#                 'nombre': '%s, %s' % (obj.profesor.apellido, obj.profesor.nombre),
#                 'id': obj.profesor.id
#             }


class PagosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pago
        fields = '__all__'


class CuentaCorrienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CuentaCorriente
        fields = '__all__'
