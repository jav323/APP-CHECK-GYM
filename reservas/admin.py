from django.contrib import admin
from .models import Clase, Horario, Reserva, Membresia

admin.site.register(Clase)
admin.site.register(Horario)
admin.site.register(Reserva)

# Clase personalizada para gestionar cómo se muestra la información de Membresía en el panel de administración.
# Se crea esta clase porque el admin por defecto no permite añadir columnas calculadas ni aplicar estilos.
# Gracias a esta personalización, se puede mostrar un estado visual (con colores) que facilita al administrador
# identificar rápidamente si una membresía está activa, próxima a caducar o ya caducada.
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "fecha_inicio", "fecha_fin", "estado_coloreado")
    list_filter = ("fecha_fin",)
    search_fields = ("usuario__username",)

admin.site.register(Membresia, MembresiaAdmin)
