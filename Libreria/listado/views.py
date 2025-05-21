from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Protege vistas contra usuarios no autenticados
from libros.models import Libro  # Modelo que usamos para mostrar datos


# ┌──────────────────────────────────────────────────────┐
# │         Vista principal del listado de libros        │
# └──────────────────────────────────────────────────────┘
@login_required(login_url='/autenticacion/logear')
def home(request):
    """
    Muestra una lista de todos los libros disponibles.
    Ideal para páginas de inicio o dashboards privados.

    Usa prefetch_related para optimizar consultas a relaciones,
    especialmente útiles si se accede frecuentemente al usuario dueño de cada libro.
    """

    # Cargamos todos los libros con su relación 'usuario' previamente cargada,
    # filtramos por usuario.
    libros = Libro.objects.prefetch_related('usuario').filter(usuario=request.user)

    # 📦 Creamos un listado iterable de libros para pasar a la plantilla
    listado_libros = list()

    for libro in list(libros):
        # Añadimos cada libro al listado (podrías agregar lógica adicional aquí)
        listado_libros.append(libro)

    # 🧾 Renderizamos la plantilla pasando el listado como contexto
    return render(request, 'listado/home.html', {"listado": listado_libros})