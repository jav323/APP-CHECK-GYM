from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path("", views.home, name="home"),

    # HORARIOS
    path("horarios/", views.listar_horarios, name="listar_horarios"),

    # LOGIN / REGISTRO
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # RESERVAS
    path("reservar/<int:horario_id>/", views.reservar_clase, name="reservar_clase"),
    path("mis-reservas/", views.mis_reservas, name="mis_reservas"),
    path("cancelar/<int:reserva_id>/", views.cancelar_reserva, name="cancelar_reserva"),
]
