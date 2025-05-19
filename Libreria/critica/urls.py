from django.urls import path
from . import views


# Nombre lógico de la aplicación para namespacing en URLs
app_name = 'critica'

"""
 📡 Rutas URL de la app 'critica'
 ────────────────────────────────────────────────
 Cada ruta conecta una URL con una vista (view)
 y tiene un nombre único para facilitar su uso en {% url %} o redirect()
"""

urlpatterns = [
    # 🏠 Página principal: lista todas las críticas y permite crear nuevas
    path('', views.critica_view, name='critica'),

    # 🛠️ Edita una crítica existente. Necesita el ID (pk) del libro criticado
    path('editar/<int:pk>/', views.editar_critica, name='editar_critica'),

    # 💥 Elimina una crítica. También necesita el ID (pk) para identificarla
    path('borrar/<int:pk>/', views.borrar_critica, name='borrar_critica'),
]