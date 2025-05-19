from django.db import models
from libros.models import Libro
from django.contrib.auth.models import User


# Modelo: Critica
# ────────────────────────────────────────────────
# Representa una crítica escrita por un usuario sobre un libro.
# Cada libro solo puede tener una crítica asociada (OneToOneField).
# La crítica también lleva registro de quién la escribió y cuándo.

class Critica(models.Model):
    # 🔗 Relación con el libro. Es única (OneToOneField), no puede haber más de una crítica por libro.
    id_libros = models.OneToOneField(
        Libro,
        on_delete=models.CASCADE,
        related_name='criticas'
    )

    # 📝 Contenido real de la crítica. Puede ser largo y detallado.
    contenido = models.TextField()

    # 👤 Usuario que creó la crítica. Puede estar vacío si se decide permitir anónimos (opcional).
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # 🕒 Fechas automáticas
    created = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated = models.DateTimeField(auto_now=True)      # Última actualización

    class Meta:
        verbose_name = "crítica"
        verbose_name_plural = "críticas"

    def __str__(self):
        """
        🧠 Identificador legible del modelo.
        Muestra algo como: 'Crítica de El nombre del viento'
        """
        return f"Crítica de {self.id_libros}"