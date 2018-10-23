from rest_framework import serializers
from .models import *
import datetime


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
    profesor = serializers.SerializerMethodField(method_name='get_profesor_data')

    class Meta:
        model = Clase
        # depth = 1
        fields = ('url', 'pk', 'nombre', 'profesor', 'dia', 'hora_inicio', 'hora_fin')

    @staticmethod
    def get_profesor_data(obj):
        return {
                'nombre': obj.profesor.nombre,
                'apellido': obj.profesor.apellido,
                'pk': obj.profesor.pk
                }


class RegistroClasesSerializer(serializers.ModelSerializer):
    # clases = ClaseSerializer(many=True, read_only=False)

    lista_alumnos = serializers.SerializerMethodField(method_name='get_lista_alumno')
    profesor = serializers.SerializerMethodField(method_name='get_profesor_data')

    class Meta:
        model = RegistroClase
        fields = ('url', 'pk', 'nombre', 'clase_orig', 'lista_alumnos', 'profesor', 'fecha', 'hora_inicio', 'hora_fin', 'estado')
        # fields = ('pk', 'alumno', 'clase')

    @staticmethod
    def get_lista_alumno(obj):
        lista_alumnos = []
        now = datetime.datetime.now()

        if now > obj.fecha: #Pasado
            alumno = Asistencia.objects.filter(clases=obj.pk)
            for al in alumno:
                lista_alumnos.append(
                    {
                        'nombre': '%s, %s' % (al.apellido, al.nombre),
                        'pk': al.pk,
                        'presente': True
                    }
                )
        elif now < obj.fecha: #Futuro
            alumno = Alumno.objects.filter(clases=obj.clase_orig)
            for al in alumno:
                lista_alumnos.append(
                    {
                        'nombre': '%s, %s' % (al.apellido, al.nombre),
                        'pk': al.pk,
                        'presente': False
                    }
                )
        else: #Presente. Hay que combinar los alumnos de la clase mas los que ya tienen asistencia
            alumno_1 = Alumno.objects.filter(clases=obj.clase_orig)
            alumno_2 = Asistencia.objects.filter(clases=obj.pk)
            alumno = (alumno_1 | alumno_2).distinct()

            for al in alumno:
                if al in alumno_2:
                    lista_alumnos.append(
                        {
                            'nombre': '%s, %s' % (al.apellido, al.nombre),
                            'pk': al.pk,
                            'presente': True
                        }
                    )
                else:
                    lista_alumnos.append(
                        {
                            'nombre': '%s, %s' % (al.apellido, al.nombre),
                            'pk': al.pk,
                            'presente': False
                        }
                    )

        return lista_alumnos

    @staticmethod
    def get_profesor_data(obj):
        return {
            'nombre': '%s, %s' % (obj.profesor.apellido, obj.profesor.nombre),
            'pk': obj.profesor.pk
        }


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