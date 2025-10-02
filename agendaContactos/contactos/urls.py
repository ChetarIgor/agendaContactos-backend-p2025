from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('agregar/', views.agregar_contacto, name='agregar_contacto'), # Página para agregar contacto
    path('lista/', views.lista_contactos, name='lista_contactos'), # Página para ver la lista de contactos
    path('editar/<int:id>/', views.editar_contacto, name='editar_contacto'), # Página para editar el contacto
    path('eliminar/<int:id>/', views.eliminar_contacto, name='eliminar_contacto'), # Página para eliminar el contacto
]

