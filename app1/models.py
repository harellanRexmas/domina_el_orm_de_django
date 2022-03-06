from tabnanny import verbose
from django.db import models

# Create your models here.
class Categoria(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descripcion
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()
    
    class Meta:
        verbose_name_plural = "Categorias"