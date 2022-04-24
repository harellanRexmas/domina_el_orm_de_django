from datetime import date
from django.db import models
from django.utils.text import slugify

class ModeloAuditoria(models.Model):
    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
    ESTADO_OPCIONES = [
        (ACTIVO, 'activo'),
        (INACTIVO, 'inactivo'),
    ]

    estado = models.CharField(max_length=8, choices=ESTADO_OPCIONES, default=ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True

# Create your models here.
class Categoria(ModeloAuditoria):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoria',
        unique=False
    )

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self, *args, **kwargs):
        super(Categoria, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categorias"

class SubCategoria(ModeloAuditoria):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Sub Categoria'
    )

    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion, self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()
    
    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria', 'descripcion')

class Persona(ModeloAuditoria):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=False, blank=False)

    @property
    def edad(self):
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return edad
    
    @property
    def nombre_completo(self):
        return "{} {}".format(self.nombre, self.apellido)

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)
    
    def save(self):
        self.nombre = self.nombre.capitalize()
        self.apellido = self.apellido.capitalize()
        super(Persona, self).save()
    
    class Meta:
        verbose_name_plural = 'Personas'

class Animal(ModeloAuditoria):
    nombre = models.CharField(max_length=10)
    patas = models.IntegerField(default=4)

    def __str__(self):
        return self.nombre
    
    def sava(self):
        self.nombre = self.nombre.upper()
        super(Animal, self).save()
    
    class Meta:
        verbose_name_plural = 'Animales'

class Libro(ModeloAuditoria):
    VIRTUAL = 'Virtual'
    FISICO = 'Fisico'
    TIPO_OPCIONES = [
        (VIRTUAL, 'Virtual'),
        (FISICO, 'Fisico'),
    ]
    nombre = models.CharField(max_length=50)
    precio = models.FloatField(default=1, help_text=' en dólares')
    peso = models.PositiveIntegerField(default=0, help_text=' en Libras')
    tipo = models.CharField(max_length=7, choices=TIPO_OPCIONES, default=FISICO)
    url_download = models.URLField(default=None)

    def __str__(self):
        return "{} ({})".format(self.nombre, self.tipo)
    
    def sava(self):
        self.nombre = self.nombre.capitalize()
        super(Animal, self).save()
    
    class Meta:
        verbose_name_plural = 'Libros'
        unique_together = ('nombre', 'tipo')

class Progenitor(ModeloAuditoria):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    padre = models.CharField(max_length=50)
    madre = models.CharField(max_length=50)

    def __str__(self):
        return '{} - {} - {}'.format(self.persona, self.madre, self.padre)
    
    class Meta:
         verbose_name_plural = 'Progenitores'

class Padre(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Hijo(models.Model):
    padre = models.ForeignKey(Padre, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "{} hijo de {}".format(self.nombre, self.padre)

class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, default='')

    def __str__(self):
        return self.titulo

    def save(self):
        self.slug = slugify(self.titulo)
        super(Publicacion, self).save()

class Articulo(models.Model):
    titular = models.CharField(max_length=100)
    publicaciones = models.ManyToManyField(Publicacion)

    def __str__(self):
        return self.titular

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    supervisor = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

class Employee(models.Model):
    nombre = models.CharField(max_length=100)
    supervisor = models.ForeignKey('app1.Employee', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

class ViewPadreHijo(models.Model):
    idpadre = models.IntegerField(primary_key=True)
    nombrepadre = models.CharField(max_length=50)
    idhijo = models.IntegerField()
    nombrehijo = models.CharField(max_length=50)

    def __str__(self) -> str:
        return '{} -> {}'.format(self.nombrepadre, self.nombrehijo)

    class Meta:
        managed = False
        db_table = 'view_padrehijo'

class NuevoNombre(models.Model):
    nombre = models.CharField(max_length=50)
    a = models.CharField(max_length=50, db_column='otro_nombre', default='')
    def __str__(self) -> str:
        return self.nombre

    class Meta:
        db_table='nuevo_nombre'

class Unico(models.Model):
    nombre = models.CharField(
        max_length=100
    )

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)
    
    @classmethod
    def truncate(cls):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Categoria)
def categoria_save(sender, **kwargs):
    print('Categoria Guardada')

@receiver(post_delete, sender=Categoria)
def categoria_delete(sender, **kwargs):
    print('Categoria Eliminada')