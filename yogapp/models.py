from django.db import models


# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, default=None, blank=True)

    def __str__(self):
        return self.nombre


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    especialidad = models.ManyToManyField(Especialidad, blank=True)
    fecha_nac = models.DateField()
    fecha_ing = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)


class Clase(models.Model):
    DOW = (
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miercoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sabado'),
        ('DO', 'Domingo'),
    )

    HORA = (
            ('08:00', '08:00'),
            ('08:30', '08:30'),
            ('09:00', '09:00'),
            ('09:30', '09:30'),
            ('10:00', '10:00'),
            ('10:30', '10:30'),
            ('11:00', '11:00'),
            ('11:30', '11:30'),
            ('12:00', '12:00'),
            ('12:30', '12:30'),
            ('13:00', '13:00'),
            ('13:30', '13:30'),
            ('14:00', '14:00'),
            ('14:30', '14:30'),
            ('15:00', '15:00'),
            ('15:30', '15:30'),
            ('16:00', '16:00'),
            ('16:30', '16:30'),
            ('17:00', '17:00'),
            ('17:30', '17:30'),
            ('18:00', '18:00'),
            ('18:30', '18:30'),
            ('19:00', '19:00'),
            ('19:30', '19:30'),
            ('20:00', '20:00'),
            ('20:30', '20:30'),
            ('21:00', '21:00')
            )

    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)#, related_name='clases')
    # alumnos = models.ManyToManyField(Alumno, blank=True) #, through='RegistroAlumno')
    dia = models.CharField(max_length=2, choices=DOW, null=True)
    hora_inicio = models.CharField(max_length=2, choices=HORA, null=True)
    hora_fin = models.CharField(max_length=2, choices=HORA, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    fecha_nac = models.DateField()
    fecha_ing = models.DateTimeField(auto_now_add=True)
    clases = models.ManyToManyField(Clase, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)


# Las clases no se borran, se desactivan.
# Por mas que exista un boton de "delete", no se muestran mas en la interfaz,
# pero continuan en la base de datos como desactivadas.
class RegistroClase(models.Model):
    fecha = models.DateField()
    profesor = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    clase = models.ForeignKey(Clase, on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)


class RegistroAlumno(models.Model):
    fecha = models.DateField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    registro = models.ForeignKey(RegistroClase, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)