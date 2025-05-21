from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Critica 
from libros.models import Libro
from .forms import Formulario_critica
from .forms_editar import Formulario_critica_editar
from django.contrib import messages


@login_required(login_url="/autenticacion/logear")
def critica_view(request):
    """
    🎯 Vista principal para crear críticas de libros.
    
    Solo usuarios logueados pueden acceder (gracias al decorador).
    
    ✅ Si es POST: intenta guardar una nueva crítica.
        - Si es válida: redirige y muestra mensaje de éxito.
        - Si no es válida: avisa que ya existe una crítica para ese libro.
    
    📖 Si es GET: muestra el formulario vacío listo para rellenar.
    
    🧠 Los libros mostrados son solo los marcados como 'leído = True'.
    """

    if request.method == 'POST':
        form = Formulario_critica(request.POST)
        # Filtramos antes de validar para que solo muestre libros propios
        form.fields['id_libros'].queryset = Libro.objects.filter(
            leido=True,
            usuario=request.user
        )
        if form.is_valid():
            critica = form.save(commit=False)
            critica.usuario = request.user  # ✅ Asignamos el usuario actual
            critica.save()
            messages.success(request, f'Crítica para "{critica.id_libros}" guardada correctamente.')
            return redirect('critica:critica')
        else:
            messages.warning(request, 'Ya existe una crítica para este libro.')
            form.fields['id_libros'].queryset = Libro.objects.filter(
              leido=True,
              usuario=request.user
            )
    else:
        form = Formulario_critica()
        form.fields['id_libros'].queryset = Libro.objects.filter(
          leido=True,
          usuario=request.user
        )

    # Mostramos solo las críticas de libros leídos
    criticas = Critica.objects.filter(
      id_libros__leido=True,
      usuario=request.user
    )

    return render(request, 'critica/critica.html', {
        'form': form,
        'criticas': criticas,
    })


@login_required(login_url="/autenticacion/logear")
def editar_critica(request, pk):
    """
    🛠️ Edita una crítica existente.
    
    Busca la crítica por su clave primaria (pk), si no existe... ¡Boom! 404.
    
    🔁 Funciona tanto para mostrar el formulario (GET) como para actualizarlo (POST).
    """

    critica = get_object_or_404(Critica, pk=pk)

    if request.method == 'POST':
        form = Formulario_critica_editar(request.POST, request.FILES, instance=critica)
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
    """
    💥 Elimina una crítica de forma segura.
    
    Muestra una confirmación antes de borrar (GET), y borra realmente en POST.
    
    🗑️ También mostramos el título del libro asociado para hacer más claro el mensaje.
    """

    critica = get_object_or_404(Critica, pk=pk)
    libro_titulo = critica.id_libros.titulo

    if request.method == 'POST':
        critica.delete()
        messages.success(request, f'Crítica para "{libro_titulo}" eliminada correctamente.')
        return redirect('critica:critica')

    return render(request, 'critica/confirmar_borrar.html', {'critica': critica})