from django.contrib import admin, messages
from django import forms
from django.http import HttpResponse
import csv

from .models import Contacto


# Formulario de Admin para asegurar normalización y validación en el admin
class ContactoAdminForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["nombre", "telefono", "correo", "direccion"]

    def clean_correo(self):
        # Normaliza a minúsculas y elimina espacios
        correo = (self.cleaned_data.get("correo") or "").strip().lower()
        return correo

    def clean_telefono(self):
        # Elimina espacios accidentales
        telefono = (self.cleaned_data.get("telefono") or "").strip()
        return telefono


# Filtro lateral para dominios de correo permitidos
class EmailDomainFilter(admin.SimpleListFilter):
    title = "Dominio de correo"
    parameter_name = "dominio"

    def lookups(self, request, model_admin):
        return [
            ("gmail.com", "Gmail"),
            ("hotmail.com", "Hotmail"),
            ("outlook.com", "Outlook"),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(correo__iendswith="@" + self.value())


# Acciones masivas
def normalizar_correos(modeladmin, request, queryset):
    actualizados = 0
    errores = 0
    for c in queryset:
        original = c.correo
        c.correo = (c.correo or "").strip().lower()
        try:
            c.full_clean()  # corre validadores del modelo
            if c.correo != original:
                c.save(update_fields=["correo"])
                actualizados += 1
        except Exception:
            errores += 1
    if actualizados:
        modeladmin.message_user(
            request, f"{actualizados} correos normalizados.", level=messages.SUCCESS
        )
    if errores:
        modeladmin.message_user(
            request, f"{errores} registro(s) no pudieron normalizarse por errores de validación.",
            level=messages.WARNING,
        )


normalizar_correos.short_description = "Normalizar correos (minúsculas y sin espacios)"


def normalizar_nombres(modeladmin, request, queryset):
    actualizados = 0
    for c in queryset:
        original = c.nombre
        # Normaliza espacios y capitaliza palabras (p. ej. 'pepito mendez' -> 'Pepito Mendez')
        c.nombre = " ".join((c.nombre or "").split()).title()
        if c.nombre != original:
            c.save(update_fields=["nombre"])
            actualizados += 1
    modeladmin.message_user(
        request, f"{actualizados} nombre(s) normalizado(s).", level=messages.SUCCESS
    )


normalizar_nombres.short_description = "Normalizar nombres (capitalización y espacios)"


def validar_seleccion(modeladmin, request, queryset):
    ok = 0
    errores = 0
    for c in queryset:
        try:
            c.full_clean()  # ejecuta todos los validadores definidos en el modelo
            ok += 1
        except Exception as e:
            errores += 1
    modeladmin.message_user(
        request, f"{ok} registro(s) válidos. {errores} con errores.",
        level=messages.INFO if errores == 0 else messages.WARNING,
    )


validar_seleccion.short_description = "Validar contactos seleccionados (aplica validadores del modelo)"


def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="contactos.csv"'
    writer = csv.writer(response)
    writer.writerow(["Nombre", "Teléfono", "Correo", "Dirección"])
    for c in queryset:
        writer.writerow([c.nombre, c.telefono, c.correo, c.direccion])
    return response


exportar_csv.short_description = "Exportar a CSV"


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    form = ContactoAdminForm

    # Listado
    list_display = ("nombre", "telefono", "correo", "direccion", "email_domain")
    list_display_links = ("nombre",)
    list_editable = ("telefono", "correo", "direccion")
    ordering = ("nombre",)
    list_per_page = 25

    # Búsqueda y filtros
    search_fields = ("nombre", "telefono", "correo")
    list_filter = (EmailDomainFilter,)

    # Acciones masivas
    actions = [normalizar_correos, normalizar_nombres, validar_seleccion, exportar_csv]

    # Campo calculado para mostrar dominio de correo
    @admin.display(description="Dominio", ordering="correo")
    def email_domain(self, obj):
        if obj.correo and "@" in obj.correo:
            return obj.correo.split("@")[-1].lower()
        return ""

    # Asegura normalización también al guardar desde el Admin
    def save_model(self, request, obj, form, change):
        obj.correo = (obj.correo or "").strip().lower()
        obj.telefono = (obj.telefono or "").strip()
        super().save_model(request, obj, form, change)
