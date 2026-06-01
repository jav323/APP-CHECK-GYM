from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # HOME
    path("", login_required(views.home), name="home"),

    # HORARIOS
    path("horarios/", login_required(views.listar_horarios), name="listar_horarios"),

    # LOGIN / LOGOUT (NO SE PROTEGEN)
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # RECUPERAR CONTRASEÑA (NO SE PROTEGE)
    path("password-reset/", views.password_reset_view, name="password_reset"),

    # RESERVAS
    path("reservar/<int:horario_id>/", login_required(views.reservar_clase), name="reservar_clase"),
    path("mis-reservas/", login_required(views.mis_reservas), name="mis_reservas"),
    path("cancelar/<int:reserva_id>/", login_required(views.cancelar_reserva), name="cancelar_reserva"),
]
