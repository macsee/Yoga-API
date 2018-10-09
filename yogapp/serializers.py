from rest_framework import serializers
from .models import *


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ('url', 'pk', 'nombre', 'descripcion')


class AlumnoSerializer(serializers.ModelSerializer):
    # registro = serializers.StringRelatedField(many=True)

    class Meta:
        model = Alumno
        fields = ('url', 'pk', 'nombre', 'apellido', 'dni', 'tel', 'fecha_nac', 'clases', 'activo')


class ProfesorSerializer(serializers.ModelSerializer):
    # clases = ClaseSerializer(many=True, read_only=False)

    class Meta:
        model = Profesor
        fields = ('url', 'pk', 'nombre', 'apellido', 'especialidad', 'dni', 'tel', 'fecha_nac')


class ClaseSerializer(serializers.ModelSerializer):
    # geofence = ProfesorSerializer(many=True)
    # geofence = serializers.CharField(source='profesor.nombre', read_only=True)
    # profesor = ProfesorSerializer()
    profesor_ = serializers.SerializerMethodField(method_name='get_profesor_data')

    class Meta:
        model = Clase
        # depth = 1
        fields = ('url', 'pk', 'nombre', 'profesor', 'profesor_', 'dia', 'hora_inicio', 'hora_fin')

    @staticmethod
    def get_profesor_data(obj):
        return {
                'nombre': obj.profesor.nombre,
                'apellido': obj.profesor.apellido,
                'pk': obj.profesor.pk
                }


class RegistroAlumnoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistroAlumno
        fields = "__all__"


class RegistroClaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistroClase
        fields = "__all__"


class ClaseAlumnoSerializer(serializers.ModelSerializer):
    # clase = serializers.SerializerMethodField(method_name='get_clase_data')
    # alumno = serializers.SerializerMethodField(method_name='get_alumno_data')
    lista_alumnos = serializers.SerializerMethodField(method_name='get_lista_alumno')
    profesor = serializers.SerializerMethodField(method_name='get_profesor_data')

    class Meta:
        model = Clase
        fields = ('url', 'pk', 'nombre', 'lista_alumnos', 'profesor', 'dia', 'hora_inicio', 'hora_fin')
        # fields = ('pk', 'alumno', 'clase')

    @staticmethod
    def get_lista_alumno(obj):
        lista_alumnos = []
        alumno = Alumno.objects.filter(clases=obj.pk)
        for al in alumno:
            lista_alumnos.append(
                {
                    'nombre': '%s, %s' % (al.apellido, al.nombre),
                    'pk': al.pk
                }
            )

        return lista_alumnos


    @staticmethod
    def get_profesor_data(obj):
        return {
            'nombre': '%s, %s' % (obj.profesor.apellido, obj.profesor.nombre),
            'pk': obj.profesor.pk
        }

    # @staticmethod
    # def get_clase_data(obj):
    #     return {'nombre': obj.clase.nombre,
    #             'profesor': '%s, %s' % (obj.clase.profesor.apellido, obj.clase.profesor.nombre),
    #             'dia': obj.clase.dia,
    #             'pk': obj.clase.pk
    #             }

    # @staticmethod
    # def get_alumno_data(obj):
    #     return {'nombre': obj.alumno.nombre,
    #             'apellido': obj.alumno.apellido,
    #             'pk': obj.alumno.pk
    #             }