import os
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User  # Modelo estándar de usuarios de Django
from PIL import Image


# ┌──────────────────────────────────────────────────────┐
# │                  CATEGORÍAS DE LIBROS                │
# └──────────────────────────────────────────────────────┘
class Categoria(models.Model):
    """
    Representa una categoría temática de libros.
    Ejemplo: Fantasía, Ciencia Ficción, Historia, etc.
    """

    nombre = models.CharField(max_length=50)  # Nombre de la categoría

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nombre  # Para mostrar el nombre en lugar del ID en admin y shell


def directorio_imagen_libro(instance, filename):
    ext = filename.split('.')[-1]
    titulo = instance.titulo or "sin_titulo"
    nombre_archivo = f"libro_{slugify(titulo[:40])}.{ext}"
    return os.path.join('libros', nombre_archivo)


# ┌──────────────────────────────────────────────────────┐
# │                    MODELO DE LIBRO                   │
# └──────────────────────────────────────────────────────┘
class Libro(models.Model):
    """
    Representa un libro en la colección del usuario.
    Incluye metadatos, contenido y estado de lectura.
    """

    # Usuario dueño del libro - relación uno a muchos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Identificador único del libro
    isbn = models.CharField(max_length=20)

    autor = models.CharField(max_length=50)
    titulo = models.CharField(max_length=50)

    # Un libro puede tener varias categorías y viceversa
    categoria = models.ManyToManyField(Categoria)

    # Contenido descriptivo o reseña del libro
    contenido = models.TextField()

    # Imagen opcional del libro (portada, por ejemplo)
    imagen = models.ImageField(upload_to=directorio_imagen_libro, null=True, blank=True)

    # Estado de lectura - útil para listados personalizados
    leido = models.BooleanField(default=True)

    # Campos de auditoría automáticos
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "libro"
        verbose_name_plural = "libros"

    def __str__(self):
        return self.titulo  # Muestra el título en lugar del ID en admin y shell
      
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Primero guardamos el modelo para asegurar que tenga imagen asociada

        if self.imagen and os.path.exists(self.imagen.path):  # Verificamos que exista el archivo
            img = Image.open(self.imagen.path)

            # Tamaño máximo deseado (ajusta estos valores según tus necesidades)
            max_width = 800
            max_height = 800

            # Redimensionar si es necesario
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.LANCZOS)

                # Guardamos la imagen redimensionada
                img.save(self.imagen.path, optimize=True, quality=85)  # Ajuste de calidad opcional
                
                
                
