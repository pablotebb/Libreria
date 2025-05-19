from django.urls import path
from . import views  # Importamos las vistas definidas en esta app


# ┌──────────────────────────────────────────────────────┐
# │         Rutas URL para la aplicación "listado"       │
# └──────────────────────────────────────────────────────┘

urlpatterns = [
    # 🏠 Página principal del listado
    # Accesible desde la ruta raíz de esta app (ej: /listado/)
    path("", views.home, name="listado"),
]