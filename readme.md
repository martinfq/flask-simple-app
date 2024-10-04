
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

---

## Estructura del proyecto

```bash
flask-app/
│
├── app.py                  # Archivo principal de la aplicación
├── venv/                   # Entorno virtual
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

## Descripción de la aplicación

Esta es una aplicación básica construida con Flask que incluye las rutas y funcionalidades simples. Ideal para entender el flujo de trabajo en Flask.

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
