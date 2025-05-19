from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Critica 
from libros.models import Libro
from .forms import Formulario_critica
from .forms_editar import Formulario_critica_editar
from django.contrib import messages

@login_required(login_url="/autenticacion/logear")
def critica_view(request):
    if request.method == 'POST':
        form = Formulario_critica(request.POST)
        if form.is_valid():
            critica = form.save()
            messages.success(request, f'Crítica para "{critica.id_libros}" guardada correctamente.')
            return redirect('critica:critica')
        else:
          messages.success(request, 'La critica del libro ya existe!')
          form.fields['id_libros'].queryset = Libro.objects.filter(leido=True)
    else:
        form = Formulario_critica()
        form.fields['id_libros'].queryset = Libro.objects.filter(leido=True)

    criticas = Critica.objects.filter(id_libros__leido=True)
    

    return render(request, 'critica/critica.html', {
        'form': form,
        'criticas': criticas,
    })

@login_required(login_url="/autenticacion/logear")
def editar_critica(request, pk):
    critica = get_object_or_404(Critica, pk=pk)
    if request.method == 'POST':
        form = Formulario_critica_editar(request.POST, instance=critica)
        if form.is_valid():
            form.save()
            messages.success(request, f'Crítica para "{critica.id_libros}" actualizada correctamente.')
            return redirect('critica:critica')
    else:
        form = Formulario_critica_editar(instance=critica)
    return render(request, 'critica/formulario.html', {
      'form': form,
      'titulo_libro': critica.id_libros.titulo
    })

@login_required(login_url="/autenticacion/logear")
def borrar_critica(request, pk):
    critica = get_object_or_404(Critica, pk=pk)
    libro_titulo = critica.id_libros.titulo
    if request.method == 'POST':
        critica.delete()
        messages.success(request, f'Crítica para "{libro_titulo}" eliminada correctamente.')
        return redirect('critica:critica')
    return render(request, 'critica/confirmar_borrar.html', {'critica': critica})