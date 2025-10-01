from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('agregar/', views.agregar_contacto, name='agregar_contacto'),
    path('listar/', views.listar_contactos, name='listar_contactos'),
    path('editar/<int:id>/', views.editar_contacto, name='editar_contacto'),
    path('eliminar/<int:id>/', views.eliminar_contacto, name='eliminar_contacto'),
]

