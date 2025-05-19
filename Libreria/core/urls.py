from django.urls import path
from . import views

# ┌──────────────────────────────────────────────┐
# │           Configuración de URLs              │
# └──────────────────────────────────────────────┘
# Este archivo define las rutas URL de la app 'core'
# y las conecta con sus respectivas vistas.

# Nombre lógico de la aplicación
# Esto permite usar namespace en las URLs, útil para {% url %} en templates o reverse() en vistas.
app_name = "core"

# ┌──────────────────────────────────────────────┐
# │          Lista de Rutas (URL Patterns)       │
# └──────────────────────────────────────────────┘
# Cada entrada en urlpatterns mapea una URL a una vista.
# Es como el mapa del tesoro de tu aplicación web.

urlpatterns = [
    # Ruta principal: Página de inicio
    # Accesible desde la raíz del dominio: http://dominio/
    path("", views.home, name="home"),
]