"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from yogapp import views
from yogapp import utils

router = DefaultRouter()
router.register(r'alumnos', views.AlumnosView, 'alumnos')
router.register(r'profesores', views.ProfesoresView, 'profesores')
router.register(r'clases', views.ClasesView, 'clases')
router.register(r'especialidades', views.EspecialidadesView, 'especialidades')
router.register(r'clase_dia', views.RegistroClasesView, 'clase_dia')
# router.register(r'clase_fecha', views.ClaseFechaView, 'clase_fecha')
router.register(r'asistencias', views.AsistenciasView, 'asistencias')
router.register(r'pagos', views.PagosView, 'pagos')
router.register(r'cuenta_corriente', views.CuentaCorrienteView, 'cuenta_corriente')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alumnos/create/<str:alumno>/', utils.create_alumno),
    path('asistencias/set', utils.set_asistencias),
    path('asistencias/get', utils.get_asistencias),
    path('asistencias/clean', utils.delete_asistencias),
    path('', include(router.urls))
]
