#  Plataforma OTT - Sistema de Streaming con Flask 

##  Descripción General 

Este proyecto consiste en el desarrollo de una plataforma OTT (Over-The-Top) tipo Netflix utilizando **Python Flask**, **SQLite**, **HTML5** y **CSS3**.

La aplicación permite a los usuarios registrarse, iniciar sesión, visualizar un catálogo de películas o series, reproducir contenido dinámicamente y mantener un historial en la sección **"Continuar viendo"**.

El sistema implementa control de suscripción (FREE / PREMIUM), validaciones backend, manejo de sesiones y persistencia de datos.

Este proyecto representa un **MVP (Producto Mínimo Viable)** funcional de una plataforma de streaming.

---

#  Objetivos del Proyecto 

## Objetivo General
Desarrollar una aplicación web que simule el funcionamiento básico de una plataforma de streaming OTT.

## Objetivos Específicos

- Implementar sistema de registro e inicio de sesión.
- Validar datos desde el backend.
- Manejar sesiones de usuario.
- Reproducir contenido dinámicamente según selección.
- Guardar historial de visualización.
- Implementar sección "Continuar viendo".
- Diferenciar acceso según tipo de suscripción.
- Aplicar diseño visual tipo plataforma de streaming.

---

#  Arquitectura del Proyecto 

El proyecto sigue una arquitectura básica tipo MVC:

- **Modelo (models.py)**: Manejo de base de datos.
- **Vista (templates)**: HTML con Jinja2.
- **Controlador (app.py)**: Lógica de negocio y rutas.

Estructura de carpetas:

```
/project
│
├── app.py
├── models.py
├── database.db
├── requirements.txt
│
├── /templates
│ ├── login.html
│ ├── registro.html
│ ├── home.html
│ ├── watch.html
| ├── catalog.html
| ├── profile.html
│
├── /static
│ ├── /css
│ │ └── styles.css
│ └── /videos 

```
---
#  Tecnologías Utilizadas 

- Python 3
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2

---

# Instalación y Configuración 

##  Clonar el repositorio 

```bash
git clone <URL_DEL_REPOSITORIO>
cd nombre_del_proyecto
```
##  Crear entorno virtual 
```bash
python -m venv venv
```
##  Instalar dependencias 
```bash
pip install flask
pip install -r requirements.txt
```
##  Ejecutar la aplicación
```bash
python app.py
flask run
```

#  Base de Datos 

El proyecto utiliza **SQLite** como base de datos local.

La base de datos se genera automáticamente al ejecutar la aplicación por primera vez.

---

##  Tablas Implementadas 

###  users 

| Campo             | Tipo      | Descripción                          |
|------------------|----------|--------------------------------------|
| id               | INTEGER  | Clave primaria (PK)                  |
| username         | TEXT     | Nombre de usuario                    |
| password         | TEXT     | Contraseña del usuario               |
| subscription_type| TEXT     | Tipo de suscripción (FREE/PREMIUM)   |

---

### movies / shows 

| Campo       | Tipo     | Descripción                          |
|------------|----------|--------------------------------------|
| id         | INTEGER  | Clave primaria (PK)                  |
| title      | TEXT     | Título de la película o serie        |
| description| TEXT     | Descripción del contenido            |
| video_url  | TEXT     | URL del video a reproducir           |

---

###  watch_history 

| Campo       | Tipo      | Descripción                                      |
|------------|----------|--------------------------------------------------|
| id         | INTEGER  | Clave primaria (PK)                              |
| user_id    | INTEGER  | Clave foránea (FK) hacia tabla users             |
| show_id    | INTEGER  | ID del contenido reproducido                     |
| show_name  | TEXT     | Nombre del contenido                             |
| video_url  | TEXT     | URL del video reproducido                        |
| watched_at | TIMESTAMP| Fecha y hora de reproducción                     |

Esta tabla permite almacenar el historial de reproducción para la funcionalidad **"Continuar viendo"**.

#  Funcionalidades Implementadas 

## Registro de Usuario 

- Validación de campos obligatorios.
- Verificación de contraseñas.
- Mensajes flash dinámicos.
- Almacenamiento de usuario en base de datos.

---

##  Inicio de Sesión 

- Validación de usuario existente.
- Verificación de contraseña.
- Creación de sesión.
- Redirección a Home.
- Manejo de mensajes flash.

---

##  Manejo de Sesiones 

Se utiliza `session` de Flask para:

- Guardar usuario autenticado.
- Guardar tipo de suscripción.
- Restringir acceso a rutas protegidas.

### Ejemplo:

```python
if "user_id" not in session:
    return redirect("/login")
```
# Validaciones Implementadas 

- Campos vacíos.
- Usuario inexistente.
- Contraseña incorrecta.
- Control de sesión activa.
- Protección de rutas.

---

# Pruebas del Sistema 

Para probar el sistema:

1. Registrar usuario nuevo.
2. Iniciar sesión.
3. Seleccionar contenido.
4. Verificar que aparezca en "Continuar viendo".
5. Probar restricción FREE / PREMIUM.

---

#  Comandos Útiles 

### Eliminar base de datos y reiniciar:

```bash
rm database.db
```