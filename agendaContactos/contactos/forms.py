from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        
    # Validación personalizada del correo
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        # Si no enviaron correo (por si acaso), devolvemos tal cual (o lanzar error si obligatorio)
        if not correo:
            return correo

        # Verificar si contiene '@'
        if '@' not in correo:
            raise forms.ValidationError('El correo debe contener un "@"')

        # --> MUY IMPORTANTE: devolver el valor validado
        return correo