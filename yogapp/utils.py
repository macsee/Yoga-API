from .filters import *
from rest_framework import response
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def set_asistencias(request):
    response = Response("")

    for key, value in request.POST.dict().items():
        js = json.loads(value)
        asist = Asistencia.objects.filter(alumno__exact=js['alumno_pk']).filter(clase_registro__exact=js['clase_registro'])
        if not asist:#Si no estaba en la tabla de asistencias
            if js["presente"]:  # Si no estaba en la tabla de asistencias y le puse presente
                print("Tengo que agregarlo como presente")
                alumno = Alumno.objects.get(id=js['alumno_pk'])
                clase_registro = RegistroClase.objects.get(id=js['clase_registro'])
                Asistencia.objects.create(alumno=alumno, fecha=js['fecha'], clase_registro=clase_registro)
                response = Response("")
                response.status_code = 200
            else: #Si no estaba en la tabla de asistencias y le puse ausente
                print("No hago nada")
        else: #Si estaba en la tabla de asistencias
            if js["presente"]: #Si estaba en la tabla de asistencias y le puse presente
                print("No hago nada")
            else: #Si estaba en la tabla de asistencias y le puse ausente
                print("Tengo que borrar un presente")
                Asistencia.objects.filter(id__exact=asist.first().id).delete()
                response = Response("")
                response.status_code = 200

    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
#
    return response

@csrf_exempt
def create_alumno(request, alumno):
    print(request)
    # for key, value in request.POST.dict().items():
    #     js = json.loads(value)
    #     print(js)


@csrf_exempt
def delete_asistencias(request):
    Asistencia.objects.all().delete()

    response = Response("Deleted!")
    response.status_code = 200
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}

    return response


@csrf_exempt
def get_asistencias(request):
    print(request.GET)
    # obj = request.GET[key]
    # lista_alumnos = []
    # now = datetime.datetime.now()
    #
    # if now.date() > obj.fecha:
    #     alumno = Asistencia.objects.filter(clase_registro=obj.id)
    #     for al in alumno:
    #         lista_alumnos.append(
    #             {
    #                 'nombre': '%s, %s' % (al.alumno.apellido, al.alumno.nombre),
    #                 'alumno_pk': al.alumno.id,
    #                 'asist_pk': al.id,
    #             }
    #         )
    # elif now.date() < obj.fecha:
    #     alumno = Alumno.objects.filter(clases=obj.clase_orig)
    #     for al in alumno:
    #         if al.activo:
    #             lista_alumnos.append(
    #                 {
    #                     'nombre': '%s, %s' % (al.apellido, al.nombre),
    #                     'alumno_pk': al.id,
    #                     'asist_pk': None,
    #                 }
    #             )
    # else:
    #     alumnos_presentes = Asistencia.objects.filter(clase_registro_id=obj.id)
    #     alumnos_clase = Alumno.objects.filter(clases=obj.clase_orig)
    #
    #     for al in alumnos_presentes:
    #         lista_alumnos.append(
    #             {
    #                 'nombre': '%s, %s' % (al.alumno.apellido, al.alumno.nombre),
    #                 'alumno_pk': al.alumno.id,
    #                 'asist_pk': al.id,
    #             }
    #         )
    #
    #     li = [x['alumno_pk'] for x in lista_alumnos]
    #
    #     for al in alumnos_clase:
    #         if al.id not in li:
    #             lista_alumnos.append(
    #                 {
    #                     'nombre': '%s, %s' % (al.apellido, al.nombre),
    #                     'alumno_pk': al.id,
    #                     'asist_pk': None,
    #                 }
    #             )
    #
    # response = Response({"lista_alumnos":lista_alumnos})
    # response.accepted_renderer = JSONRenderer()
    # response.accepted_media_type = "application/json"
    # response.renderer_context = {}
#
    return response