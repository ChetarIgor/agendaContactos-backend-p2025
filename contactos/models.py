from django.db import models
from django.core.validators import RegexValidator

# Validador de teléfono
phone_validator = RegexValidator(
    regex=r'^\+569\d{8}$',
    message="El número debe comenzar con +569 y tener 8 dígitos después (ej: +56912345678)."
)

# Validador de correo
email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@(gmail\.com|hotmail\.com|outlook\.com)$',
    message="El correo debe ser Gmail, Hotmail o Outlook(ej: usuario@gmail.com o usuario@hotmail.com)."
)

class Contacto(models.Model):  #Crea Contacto en un tabla de BD
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=12,
        validators=[phone_validator],
        unique=True,
        error_messages={
            "unique": "Ya existe un contacto con este teléfono.",
        }        
    )
    correo = models.CharField(
        max_length=100,
        validators=[email_validator],
        unique=True,
        error_messages={
            "unique": "Ya existe un contacto con este correo.",
        }    
    )
    direccion = models.CharField(max_length=200)

    def __str__(self):  
        return self.nombre 
