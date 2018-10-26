from django.db import models
import datetime
from datetime import date, timedelta

# Create your models here.


def create_clases(obj):
    dias = ["LU", "MA", "MI", "JU", "VI", "SA", "DO"]
    dstart = date.today()
    dend = date.today() + datetime.timedelta(days=30)

    for x in range((dend-dstart).days + 1):
        fecha = dstart + timedelta(days=x)
        if dias[fecha.weekday()] == obj.dia:
            RegistroClase.objects.create(fecha=fecha, profesor=obj.profesor, clase_orig=obj, hora_inicio=obj.hora_inicio, hora_fin=obj.hora_fin)


def update_clases(obj):
    dstart = date.today()

    RegistroClase.objects.filter(clase_orig__pk__iexact=obj.pk).filter(fecha__lte=dstart).delete()
    create_clases(obj)


def delete_clases(obj):
    dstart = date.today()

    RegistroClase.objects.filter(clase_orig__pk__iexact=obj.pk).filter(fecha__gte=dstart).delete()


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    dni = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    especialidad = models.ManyToManyField(Especialidad, blank=True)
    fecha_nac = models.DateField(blank=True, null=True)
    fecha_ing = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)


class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True)#, related_name='clases')
    dia = models.CharField(max_length=2)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activa = models.BooleanField(default=True)
    # alumnos = models.ManyToManyField(Alumno, blank=True) #, through='RegistroAlumno')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):

        if self.pk is None:
            print("Creating")
            super(Clase, self).save(*args, **kwargs)
            create_clases(self)
        else:
            print("Updating")
            super(Clase, self).save(*args, **kwargs)
            update_clases(self)

    def delete(self, *args, **kwargs):
        delete_clases(self)
        super(Clase, self).delete(*args, **kwargs)


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    dni = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    fecha_nac = models.DateField(blank=True, null=True)
    fecha_ing = models.DateTimeField(auto_now_add=True, blank=True)
    clases = models.ManyToManyField(Clase, blank=True)
    tel_contacto = models.CharField(max_length=100, blank=True)
    obra_social = models.CharField(max_length=100, blank=True)
    antecedentes = models.TextField(max_length=500, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)


class CuentaCorriente(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, null=True)
    valor = models.IntegerField()  # positivo o negativo (debito o credito)
    concepto = models.CharField(max_length=100)
    fecha = models.DateField()
    last_update = models.DateTimeField(auto_now_add=True, blank=True)


class Pago(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, null=True)
    valor_total = models.IntegerField(default=0)
    valor_pagado = models.IntegerField(default=0)
    concepto = models.CharField(max_length=100)
    fecha = models.DateField()
    last_update = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):

        if self.valor_pagado != 0:
            print("Debito y Credito")
            CuentaCorriente.objects.create(alumno=self.alumno, valor=-1*self.valor_total, concepto=self.concepto, fecha=self.fecha)

        CuentaCorriente.objects.create(alumno=self.alumno, valor=self.valor_pagado, concepto=self.concepto,
                                       fecha=self.fecha)


class RegistroClase(models.Model):
    clase_orig = models.ForeignKey(Clase, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True)  # , related_name='clases')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=100, blank=True)


class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    clase_registro = models.ForeignKey(RegistroClase, on_delete=models.SET_NULL, null=True)

# Echar un vistazo a "post_save" en documentacion de Django para poder realizar acciones luego de savear datos.
# Por ejemplo, insertar informacion en una tabla registro que mantenga un diario de las modificaciones en la base de datos.
# O para la tabla de clases por dia que deben generarse para una determinada cantidad de meses.
# Respecto de las Clases, hay que decidir si conviene permitir editarlas o no. Pensar el caso de que una clase en particular
# sea dictada por una profesora diferente a la que habitualmente da esa clase, entonces en el registro de asistencias por ahi
# es conveniente no guardar el id de clase sino una copia textual de los datos


# Las clases no se borran, se desactivan.
# Por mas que exista un boton de "delete", no se muestran mas en la interfaz,
# pero continuan en la base de datos como desactivadas.