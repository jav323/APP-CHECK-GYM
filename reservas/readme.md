# CHECK‑GYM

CHECK‑GYM es una aplicación web desarrollada como proyecto de TFG para el ciclo de Desarrollo de Aplicaciones Multiplataforma. Su objetivo es digitalizar la gestión de un gimnasio y permitir que los usuarios puedan consultar horarios, reservar clases y gestionar sus reservas de manera sencilla. La idea principal es sustituir procesos manuales por un sistema claro, ordenado y accesible tanto para usuarios como para administradores.

## Descripción del proyecto

La aplicación permite que un usuario se registre o inicie sesión, consulte los horarios disponibles y reserve actividades. También puede ver sus reservas, cancelarlas y comprobar si quedan plazas libres. El sistema organiza internamente actividades, horarios, usuarios y reservas para que todo quede registrado y actualizado automáticamente. El diseño está pensado para que cualquier persona pueda usarlo sin necesidad de conocimientos técnicos.

## Tecnologías utilizadas

El proyecto está desarrollado con Python y Django, que gestionan la lógica del sistema y la comunicación con la base de datos. La base de datos utilizada es SQLite. La interfaz está construida con HTML, CSS y JavaScript. El proyecto utiliza un entorno virtual de Python y control de versiones con Git y GitHub.

## Instalación y ejecución

Para ejecutar el proyecto en local, se deben seguir estos pasos:

- Clonar el repositorio:
  `git clone https://github.com/jav323/APP-CHECK-GYM`
- Entrar en el directorio del proyecto:
  `cd APP-CHECK-GYM`
- Crear un entorno virtual:
  `python -m venv entorno_virtual`
- Activarlo en Windows:
  `entorno_virtual\Scripts\activate`
- Instalar dependencias:
  `pip install -r requirements.txt`
- Ejecutar el servidor:
  `python manage.py runserver`

Una vez hecho esto, la aplicación estará disponible en el navegador en la dirección que indique Django.

## Estructura del proyecto

El proyecto está dividido en varias aplicaciones internas. Una gestiona las reservas y otra gestiona los usuarios. Cada aplicación contiene sus modelos, vistas, rutas y plantillas. Además, existe una carpeta de archivos estáticos y otra de plantillas generales. La estructura está pensada para que el código sea fácil de mantener y ampliar.

## Manual de uso

Este manual explica cómo utilizar CHECK‑GYM tanto desde el punto de vista de un usuario normal como desde el de un administrador. Está pensado para que cualquier persona pueda probar la aplicación sin conocer previamente el proyecto.

### Uso como administrador

El administrador es quien prepara el sistema para que funcione correctamente. Los usuarios normales no pueden crear cuentas ni gestionar actividades, así que el administrador debe configurar todo antes de que la aplicación pueda usarse.

- Crear un superusuario:
  `python manage.py createsuperuser`
- Acceder al panel de administración:
  `http://127.0.0.1:8000/admin`
- Crear usuarios normales desde el panel.
- Crear actividades y horarios para que aparezcan en la aplicación.
- Supervisar reservas, modificarlas o eliminarlas si es necesario.

El administrador controla toda la información interna del sistema.

### Uso como usuario normal

Una vez que el administrador ha creado una cuenta, el usuario puede entrar en la aplicación y utilizarla de forma sencilla.

- Iniciar sesión con su nombre y contraseña.
- Consultar los horarios disponibles.
- Reservar una actividad.
- Ver sus reservas en la sección “Mis reservas”.
- Cancelar una reserva si no va a asistir.

El objetivo es que cualquier persona pueda gestionar sus actividades sin depender del personal del gimnasio.

## Qué debe comprobar alguien que quiere probar la aplicación

Si alguien quiere evaluar el proyecto o simplemente probarlo, se recomienda:

- Crear un administrador y acceder al panel.
- Crear uno o dos usuarios de prueba.
- Crear varias actividades y horarios.
- Iniciar sesión como usuario normal.
- Reservar una actividad.
- Comprobar que aparece en “Mis reservas”.
- Cancelar la reserva y verificar que desaparece.
- Revisar que la interfaz es clara y que no hay errores.

Este recorrido permite comprobar que el sistema cumple su función principal: gestionar un gimnasio de forma digital, ordenada y accesible.

## Estado del proyecto

El proyecto está finalizado y preparado para su entrega como TFG. Incluye todas las funciones necesarias: autenticación, consulta de horarios, reservas y gestión de las mismas. También se ha actualizado el diseño para que la experiencia sea más clara y agradable.

## Autor

Javi — 2º DAM
Proyecto TFG 2026