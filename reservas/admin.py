from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from .models import Clase, Horario, Reserva, Membresia

class ClaseAdmin(admin.ModelAdmin):
    list_display = ("nombre", "aforo_maximo")
    search_fields = ("nombre",)


admin.site.register(Clase, ClaseAdmin)
admin.site.register(Reserva)


class HorarioAdminForm(forms.ModelForm):
    aforo_maximo = forms.IntegerField(label="Aforo máximo", min_value=0)

    class Meta:
        model = Horario
        fields = ("clase", "dia", "hora", "duracion_minutos", "aforo_maximo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["aforo_maximo"].initial = self.instance.clase.aforo_maximo

    def save(self, commit=True):
        horario = super().save(commit=commit)
        aforo_maximo = self.cleaned_data["aforo_maximo"]
        if horario.clase.aforo_maximo != aforo_maximo:
            horario.clase.aforo_maximo = aforo_maximo
            horario.clase.save(update_fields=["aforo_maximo"])
        return horario


class HorarioAdmin(admin.ModelAdmin):
    form = HorarioAdminForm
    list_display = ("clase", "dia", "hora", "aforo_actual", "aforo_ocupado_admin", "aforo_maximo_admin")
    readonly_fields = ("aforo_actual",)
    search_fields = ("clase__nombre",)
    list_filter = ("clase", "dia")
    fields = ("clase", "dia", "hora", "duracion_minutos", "aforo_maximo", "aforo_actual")

    def aforo_ocupado_admin(self, obj):
        return obj.aforo_ocupado

    aforo_ocupado_admin.short_description = "Aforo ocupado"

    def aforo_maximo_admin(self, obj):
        return obj.clase.aforo_maximo

    aforo_maximo_admin.short_description = "Aforo máximo"


admin.site.register(Horario, HorarioAdmin)

# Clase personalizada para gestionar cómo se muestra la información de Membresía en el panel de administración.
# Se crea esta clase porque el admin por defecto no permite añadir columnas calculadas ni aplicar estilos.
# Gracias a esta personalización, se puede mostrar un estado visual (con colores) que facilita al administrador
# identificar rápidamente si una membresía está activa, próxima a caducar o ya caducada.
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "fecha_inicio", "fecha_fin", "estado_coloreado")
    list_filter = ("fecha_fin",)
    search_fields = ("usuario__username",)

    def changelist_view(self, request, extra_context=None):
        context = {
            **self.admin_site.each_context(request),
            "title": "Membresías",
            "message": "En construccion",
            "back_url": "../",
        }
        return TemplateResponse(request, "admin/en_construccion.html", context)

    def add_view(self, request, form_url="", extra_context=None):
        context = {
            **self.admin_site.each_context(request),
            "title": "Membresías",
            "message": "En construccion",
            "back_url": "../",
        }
        return TemplateResponse(request, "admin/en_construccion.html", context)

admin.site.register(Membresia, MembresiaAdmin)
