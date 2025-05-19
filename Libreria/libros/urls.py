from django.urls import path
from . import views  # Importamos las vistas definidas en esta app

# ┌──────────────────────────────────────────────────────┐
# │               Nombre lógico de la aplicación         │
# └──────────────────────────────────────────────────────┘
app_name = 'libro'  # Esto permite usar namespace en las URLs (ej: {% url 'libro:libros' %})


# ┌──────────────────────────────────────────────────────┐
# │              Definición de rutas URL                 │
# └──────────────────────────────────────────────────────┘
urlpatterns = [
    # 📚 Página principal de libros
    # Muestra todos los libros y el formulario para añadir uno nuevo
    path("", views.libro_view, name="libros"),

    # ✏️ Edición de un libro específico
    # La ruta incluye una clave primaria (pk) para identificar el libro a editar
    path('editar/<int:pk>/', views.editar_libro, name='editar_libro'),

    # ❌ Eliminación de un libro
    # Similar a la edición, usamos la pk para seleccionar el libro a borrar
    path('borrar/<int:pk>/', views.borrar_libro, name='borrar_libro'),
]