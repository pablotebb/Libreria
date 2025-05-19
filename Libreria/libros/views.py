from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Libro
from .forms import Formulario_libros
from django.contrib import messages

@login_required(login_url='/autenticacion/logear')
def libro_view(request):
  if request.method == 'POST':
    form = Formulario_libros(request.POST)
    if form.is_valid():
      libro = form.save(commit=False)
      libro.usuario = request.user  # Asignamos el usuario logueado
      libro.save()
      form.save_m2m()  # Necesario para ManyToManyFields como 'categoria'
      messages.success(request, 'Libro creado exitosamente.')
      return redirect('libro:libros')
    else:
      messages.error(request, 'Hubo errores al crear el libro. Por favor corrige los campos.')
      print('Errores:', form.errors)
      return redirect('libro:libros')
  else:
    form = Formulario_libros()

    libros = Libro.objects.all()  

    return render(request, 'libros/libro.html', {
        'form': form,
        'libros': libros,
    })

@login_required(login_url='/autenticacion/logear')
def editar_libro(request, pk):
  libro = get_object_or_404(Libro, pk=pk)
  if request.method == 'POST':
    form = Formulario_libros(request.POST, instance=libro)
    if form.is_valid():
      libro = form.save(commit=False)
      libro.usuario = request.user  # Asignamos el usuario logueado
      libro.save()
      form.save_m2m()  # Necesario para ManyToManyFields como 'categoria'
      messages.success(request, 'Libro actualizado correctamente.')
      return redirect('libro:libros')
    else:
      messages.error(request, 'Hubo errores al actualizar el libro.')
      return render(request, 'libros/formulario.html', {'form': form})
  else:
    # Método GET: mostramos el formulario con los datos actuales
    form = Formulario_libros(instance=libro)
    return render(request, 'libros/formulario.html', {'form': form})

@login_required(login_url='/autenticacion/logear')
def borrar_libro(request, pk):
  libro = get_object_or_404(Libro, pk=pk)
  if request.method == 'POST':
    libro.delete()
    messages.success(request, 'Libro eliminado correctamente.')
    return redirect('libro:libros')
  return render(request, 'libros/confirmar_borrar.html', {'libro': libro})