
# Flask App - Simple Application

Este es un proyecto básico de una aplicación web utilizando Flask.

## Requisitos

- Python 3.x

## Configuración del entorno de desarrollo

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-repositorio/flask-app.git
cd flask-app
```

### 2. Crear un entorno virtual

Se recomienda crear un entorno virtual para evitar conflictos de dependencias.

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

- En Windows:

```bash
venv\Scripts\activate
```

- En macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

Una vez activado el entorno virtual, instala las dependencias necesarias desde el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

Si no tienes un archivo `requirements.txt`, puedes generarlo con las dependencias necesarias para tu aplicación:

```bash
pip freeze > requirements.txt
```

### 5. Iniciar la aplicación

Para iniciar la aplicación Flask, ejecuta el archivo principal, normalmente llamado `app.py` o `main.py`.

```bash
python app.py
```

### 6. Acceder a la aplicación

La aplicación estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000) de forma local.

See puede crear usuarios o utilizar los que ya tiene la base de datos
Credenciales
email: pedro@gmail.com |contraseña: 123456
---

## Estructura del proyecto

La aplicacion en general tiene una arquitectura MVC
La arquitectura MVC se divide en tres componentes:

Modelo: Gestiona los datos y la lógica de negocio. Carpetas models,services

Vista: Muestra la interfaz de usuario y presenta los datos. Carpetas templates, static

Controlador: Actúa como intermediario, procesando las solicitudes del usuario y actualizando el modelo y la vista. Carpeta controllers
```bash
app-usuarios/
│
├── app.py                  # Archivo principal de la aplicación
├── .venv/                  # Entorno virtual
├── config                  # Archivo para la configuracion de la app
├── controllers             # Carpeta de las rutas/endpoints
├── instance                # Carpeta donde se almacenara la base de datos
├── models                  # Carpeta de las entidades
├── services                # Carpeta de los servicios
├── static                  # Archivos estaticos
├── templates               # Archivos HTML
├── tests                   # Testing
├── .env                    # Archivo necesario para variables de entorno
└── README.md                # Este archivo

```

## Descripción de la aplicación

Esta es una aplicación básica construida con Flask 
CRUD de Usuarios: Permite crear, leer, actualizar y eliminar usuarios en una base de datos SQLite.

Los usuarios tienen atributos como nombre, email y contraseña.

Autenticación de Usuarios:

Los usuarios pueden registrarse y loguearse utilizando su email y contraseña.
Al iniciar sesión, se guarda su nombre en la sesión para personalizar la experiencia.

Perfil de Usuario:

Después de iniciar sesión, los usuarios pueden acceder a una página de perfil donde pueden editar su información personal y también tienen la opción de eliminar su cuenta.

Interfaz de Usuario:

La aplicación utiliza plantillas HTML con una barra de navegación que cambia según si el usuario está logeado o no.
Se incluye una barra de búsqueda que permite buscar usuarios por nombre.

Navegación:

El navbar incluye enlaces a la página de inicio y a la página de login, y muestra el nombre del usuario y un botón de perfil cuando el usuario está autenticado.

Manejo de Sesiones:

Utiliza sesiones para mantener el estado del usuario, asegurando que solo los usuarios autenticados puedan acceder a ciertas funcionalidades, como editar su perfil.


## Librerias necesarias
Se encuentra en el archivo requierements.txt, para mas infomacion son las siguientes:
- blinker==1.8.2
- click==8.1.7
- colorama==0.4.6
- Flask==3.0.3
- Flask-SQLAlchemy==3.1.1
- greenlet==3.1.1
- itsdangerous==2.2.0
- Jinja2==3.1.4
- MarkupSafe==2.1.5
- python-dotenv==1.0.1
- SQLAlchemy==2.0.35
- typing_extensions==4.12.2
- Werkzeug==3.0.4
- WTForms~=3.1.2

## Comandos útiles

- Desactivar el entorno virtual:

```bash
deactivate
```

- Generar un archivo de dependencias:

```bash
pip freeze > requirements.txt
```

---

## Contribuciones

Si deseas contribuir, por favor, abre un "Pull Request" o reporta problemas en la sección de "Issues".

---

## Licencia

Este proyecto está bajo la Licencia MIT.
