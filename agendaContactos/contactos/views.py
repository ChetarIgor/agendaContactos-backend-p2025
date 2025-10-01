from django.shortcuts import render, get_object_or_404, redirect
from .models import Contacto
from .forms import ContactoForm

# Vista de inicio
def inicio(request):
    return render(request, 'contactos/inicio.html')

# Vista para agregar un contacto
def agregar_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_contactos')
    else:
        form = ContactoForm()
    return render(request, 'contactos/agregar_contacto.html', {'form': form})

# Vista para listar contactos
def listar_contactos(request):
    contactos = Contacto.objects.all()
    return render(request, 'contactos/listar_contactos.html', {'contactos': contactos})

# Vista para editar un contacto
def editar_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('listar_contactos')
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'contactos/editar_contacto.html', {'form': form})

# Vista para eliminar un contacto
def eliminar_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        contacto.delete()
        return redirect('listar_contactos')
    return render(request, 'contactos/eliminar_contacto.html', {'contacto': contacto})

