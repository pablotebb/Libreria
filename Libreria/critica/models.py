from django.db import models
from libros.models import Libro

# Create your models here.

class Critica(models.Model):
  id_libros = models.OneToOneField(Libro, on_delete=models.CASCADE, related_name='criticas')
  contenido = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  class Meta:
    verbose_name = "crítica"
    verbose_name_plural = "críticas"

  def __str__(self):
    return f"Crítica de {self.id_libros}"
 
