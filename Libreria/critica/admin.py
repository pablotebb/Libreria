from django.contrib import admin
from .models import Critica


# 👮‍♂️ Panel de administración: CriticaAdmin
# ────────────────────────────────────────────────
# Configuración del modelo Critica en el admin de Django.
# Campos 'created' y 'updated' son de solo lectura.

class CriticaAdmin(admin.ModelAdmin):
    # 🔐 Estos campos no se pueden editar desde el admin
    readonly_fields = ("created", "updated")


# 📦 Registramos el modelo Critica junto con su configuración personalizada
admin.site.register(Critica, CriticaAdmin)