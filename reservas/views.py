from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Horario, Reserva


# -----------------------------
# HOME
# -----------------------------
def home(request):
    return render(request, "home.html")


# -----------------------------
# LOGIN / REGISTRO / LOGOUT
# -----------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("listar_horarios")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
            return redirect("login")
        else:
            messages.error(request, "Revisa los datos introducidos.")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# -----------------------------
# FUNCIONALIDAD DEL GIMNASIO
# -----------------------------
def listar_horarios(request):
    horarios = Horario.objects.all().order_by("dia", "hora")

    # Añadimos un atributo booleano a cada horario
    if request.user.is_authenticated:
        for h in horarios:
            h.ya_reservado = h.reserva_set.filter(usuario=request.user).exists()
    else:
        for h in horarios:
            h.ya_reservado = False

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
