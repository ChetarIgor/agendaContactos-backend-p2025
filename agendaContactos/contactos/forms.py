from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):   #Crea un formulario de Contacto
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ejemplo: Pepito Mendez'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ejemplo: +56912345678'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Ejemplo: pepito@gmail.com'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ejemplo: Calle Wachafa 1122, Renca'}),
        }