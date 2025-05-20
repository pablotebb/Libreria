from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # Protege vistas contra usuarios no autenticados
from .models import Libro
from .forms import Formulario_libros
from django.contrib import messages  # Para mensajes flash al usuario

# ┌──────────────────────────────────────────────────────┐
# │     VISTA PRINCIPAL: Mostrar libros + formulario     │
# └──────────────────────────────────────────────────────┘
@login_required(login_url='/autenticacion/logear')
def libro_view(request):
    """
    Muestra todos los libros y permite añadir uno nuevo.
    - Si el método es POST: procesa el formulario.
    - Si es GET: muestra el formulario vacío y la lista de libros.
    """

    if request.method == 'POST':
        form = Formulario_libros(request.POST, request.FILES)

        if form.is_valid():
            libro = form.save(commit=False)
            libro.usuario = request.user  # Asignamos el autor del libro como el usuario actual
            libro.save()
            form.save_m2m()  # Guardamos relaciones ManyToMany (ej: categorías)

            messages.success(request, 'Libro creado exitosamente.')
            return redirect('libro:libros')

        else:
            messages.error(request, 'Hubo errores al crear el libro. Por favor corrige los campos.')
            print('Errores:', form.errors)  # Útil para debugging rápido
            return render(request, 'libros/libro.html', {
                'form': form,
                'libros': Libro.objects.all(), 
            })

    else:
        form = Formulario_libros()
        libros = Libro.objects.all()  # Obtenemos todos los libros para mostrarlos

        return render(request, 'libros/libro.html', {
            'form': form,
            'libros': libros,
        })


# ┌──────────────────────────────────────────────────────┐
# │                EDITAR UN LIBRO EXISTENTE             │
# └──────────────────────────────────────────────────────┘
@login_required(login_url='/autenticacion/logear')
def editar_libro(request, pk):
    """
    Permite editar un libro existente.
    - Carga los datos actuales en el formulario.
    - Actualiza si se envía correctamente.
    """
    libro = get_object_or_404(Libro, pk=pk)

    if request.method == 'POST':
        form = Formulario_libros(request.POST, request.FILES, instance=libro)

        if form.is_valid():
            libro = form.save(commit=False)
            libro.usuario = request.user  # Aseguramos que el autor siga siendo el mismo
            libro.save()
            form.save_m2m()  # Actualizamos las relaciones ManyToMany

            messages.success(request, 'Libro actualizado correctamente.')
            return redirect('libro:libros')

        else:
            messages.error(request, 'Hubo errores al actualizar el libro.')
            return render(request, 'libros/formulario.html', {'form': form})

    else:
        # Mostramos el formulario con los datos cargados
        form = Formulario_libros(instance=libro)
        return render(request, 'libros/formulario.html', {'form': form})


# ┌──────────────────────────────────────────────────────┐
# │                BORRAR UN LIBRO EXISTENTE             │
# └──────────────────────────────────────────────────────┘
@login_required(login_url='/autenticacion/logear')
def borrar_libro(request, pk):
    """
    Elimina un libro tras confirmación del usuario.
    - GET: muestra una página de confirmación.
    - POST: elimina el libro y redirige a la lista.
    """
    libro = get_object_or_404(Libro, pk=pk)

    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente.')
        return redirect('libro:libros')

    return render(request, 'libros/confirmar_borrar.html', {'libro': libro})