from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string

from .forms import LoginForm
from .models import Horario, Reserva


# -----------------------------
# HOME (PROTEGIDA)
# -----------------------------
@login_required
def home(request):
    return render(request, "home.html")


# -----------------------------
# LOGIN / LOGOUT
# -----------------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("listar_horarios")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# -----------------------------
# RECUPERAR CONTRASEÑA
# -----------------------------
def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No existe ningún usuario con ese email.")
            return redirect("password_reset")

        # Generar nueva contraseña aleatoria
        nueva_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        user.set_password(nueva_pass)
        user.save()

        # Enviar email con la nueva contraseña
        send_mail(
            subject="Recuperación de contraseña - CHECK GYM",
            message=f"Tu nueva contraseña es: {nueva_pass}",
            from_email="noreply@gym.com",
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Se ha enviado una nueva contraseña a tu email.")
        return redirect("login")

    return render(request, "password_reset.html")


# -----------------------------
# FUNCIONALIDAD DEL GIMNASIO
# -----------------------------
@login_required
def listar_horarios(request):
    horarios = Horario.objects.all().order_by("dia", "hora")

    for h in horarios:
        h.ya_reservado = h.reserva_set.filter(usuario=request.user).exists()

    return render(request, "listar_horarios.html", {"horarios": horarios})


@login_required
def reservar_clase(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)

    try:
        reserva = Reserva(usuario=request.user, horario=horario)
        reserva.save()
        messages.success(request, "Reserva realizada correctamente.")
    except ValidationError as e:
        messages.error(request, e.message)
    except Exception:
        messages.error(request, "No se pudo realizar la reserva.")

    return redirect("listar_horarios")


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    try:
        reserva.cancelar()
        messages.success(request, "Reserva cancelada correctamente.")
    except Exception:
        messages.error(request, "No se pudo cancelar la reserva.")

    return redirect("mis_reservas")


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by(
        "horario__dia", "horario__hora"
    )
    return render(request, "mis_reservas.html", {"reservas": reservas})
