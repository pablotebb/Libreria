from django.db import models
from django.contrib.auth.models import User  # Modelo estándar de usuarios de Django


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
    imagen = models.ImageField(upload_to="libros", null=True, blank=True)

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