from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.html import format_html
from django.core.exceptions import ValidationError

# Modelo que representa cada tipo de clase del gimnasio
class Clase(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    aforo_maximo = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    dia = models.DateField()
    hora = models.TimeField()
    duracion_minutos = models.PositiveIntegerField(default=60)
    aforo_actual = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.clase.nombre} - {self.dia} {self.hora}"

    @property
    def aforo_ocupado(self):
        return self.reserva_set.count()

    @property
    def aforo_disponible(self):
        return max(self.clase.aforo_maximo - self.aforo_ocupado, 0)

    def actualizar_aforo_actual(self):
        self.aforo_actual = self.aforo_ocupado
        self.save(update_fields=["aforo_actual"])


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'horario'],
                name='unique_reserva_usuario_horario'
            )
        ]

    def clean(self):
        if not self.usuario.is_active:
            raise ValidationError("No puedes reservar porque tu membresía no está activa.")

        if self.horario.aforo_ocupado >= self.horario.clase.aforo_maximo:
            raise ValidationError("No quedan plazas disponibles para esta clase.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.horario.actualizar_aforo_actual()

    def cancelar(self):
        self.delete()
        self.horario.actualizar_aforo_actual()

    def __str__(self):
        return f"{self.usuario.username} → {self.horario}"


class Membresia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def esta_activa(self):
        return self.fecha_fin >= date.today()

    def estado_coloreado(self):
        hoy = date.today()
        if self.fecha_fin < hoy:
            return format_html("<span style='color:red; font-weight:bold;'>Caducada</span>")
        elif (self.fecha_fin - hoy).days <= 5:
            return format_html("<span style='color:orange; font-weight:bold;'>Próxima a caducar</span>")
        else:
            return format_html("<span style='color:green; font-weight:bold;'>Activa</span>")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.usuario.is_active = self.esta_activa()
        self.usuario.save()

    def __str__(self):
        return f"Membresía de {self.usuario.username}"
