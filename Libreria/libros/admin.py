from django.contrib import admin
from .models import Categoria, Libro


# ┌──────────────────────────────────────────────────────┐
# │         Configuración personalizada del Admin        │
# └──────────────────────────────────────────────────────┘

# Estas clases permiten personalizar cómo se muestran y manejan los modelos
# dentro del panel de administración de Django.


class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Categoria en el admin.
    - Campos 'created' y 'updated' marcados como solo lectura.
    """
    readonly_fields = ("created", "updated")  # Evita edición manual de campos automáticos


class LibroAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Libro en el admin.
    - Campos 'created' y 'updated' también son de solo lectura.
    """
    readonly_fields = ("created", "updated")  # Protege campos generados automáticamente


# ───── Registro de modelos en el panel de administración ─────

admin.site.register(Categoria, CategoriaAdmin)  # Registramos Categoria con su configuración
admin.site.register(Libro, LibroAdmin)          # Registramos Libro con su configuración