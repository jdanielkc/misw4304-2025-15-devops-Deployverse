# Blacklist Service API 🚫📧

Servicio REST para la gestión de listas negras de correos electrónicos. Permite agregar emails a una blacklist y verificar si un email específico está en la lista.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Despliegue en AWS Elastic Beanstalk](#despliegue-en-aws-elastic-beanstalk)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Postman Collection](#postman-collection)
- [Base de Datos](#base-de-datos)
- [Contribución](#contribución)

## ✨ Características

- ✅ Agregar emails a la blacklist con información detallada
- ✅ Verificar si un email está en la blacklist
- ✅ Autenticación mediante Bearer Token
- ✅ Validación de datos de entrada
- ✅ Manejo de errores robusto
- ✅ Endpoint de salud para monitoreo
- ✅ Base de datos SQLite/PostgreSQL compatible

## 🛠️ Tecnologías

- **Python 3.13.3**
- **Flask 3.0.3** - Framework web
- **Flask-RESTful** - Extensión para APIs REST
- **SQLAlchemy** - ORM para base de datos
- **Flask-SQLAlchemy** - Integración SQLAlchemy con Flask
- **Marshmallow** - Serialización/deserialización de datos
- **psycopg2-binary** - Driver PostgreSQL
- **pytest** - Framework de testing
- **pytest-cov** - Cobertura de código

## 📁 Estructura del Proyecto

```
blacklist-service/
├── .ebextensions/            # Configuración AWS Elastic Beanstalk
│   ├── flask.config         # Variables de entorno y WSGI
│   └── db-migrate.config    # Comandos de inicialización BD
├── src/
│   ├── __init__.py
│   ├── app.py                 # Aplicación principal Flask
│   ├── database.py            # Configuración de base de datos
│   ├── models.py              # Modelos SQLAlchemy
│   ├── schemas.py             # Esquemas Marshmallow
│   └── resources/
│       ├── __init__.py
│       ├── blacklist_resource.py       # Endpoint GET (verificar)
│       └── blacklist_check_resource.py # Endpoint POST (agregar)
├── test/
│   ├── test_blacklist_get.py    # Tests endpoint GET
│   ├── test_blacklist_post.py   # Tests endpoint POST
│   ├── test_error_cases.py      # Tests casos de error
│   └── test_health.py           # Tests endpoint salud
├── application.py              # Punto de entrada para AWS EB
├── requirements.txt            # Dependencias Python
├── runtime.txt                # Versión Python para despliegue
├── pytest.ini                # Configuración pytest
├── .ebignore                  # Archivos a ignorar en despliegue
└── Blacklist_API_Postman_Collection.json
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.13.3 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**

   ```bash
   git clone <repository-url>
   cd misw4304-2025-15-devops-Deployverse/blacklist-service
   ```

2. **Crear entorno virtual**

   ```bash
   cd ..
   python -m venv .venv
   ```

3. **Activar entorno virtual**

   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

4. **Instalar dependencias**
   ```bash
   cd blacklist-service
   pip install -r requirements.txt
   ```

## ⚙️ Configuración

### Variables de entorno

Crear un archivo `.env` (opcional) con las siguientes variables:

```env
# Token de autenticación
STATIC_TOKEN=BearerToken123

# Base de datos (opcional, por defecto usa SQLite)
DATABASE_URL=sqlite:///local.db

# JWT Secret (opcional)
JWT_SECRET_KEY=secret123
```

### Configuración por defecto

- **Puerto**: 5000
- **Host**: 0.0.0.0 (todas las interfaces)
- **Base de datos**: SQLite local (`local.db`)
- **Token**: `BearerToken123`

## 🎯 Uso

### Ejecutar la aplicación

**Opción 1: Desarrollo local (recomendado)**

```bash
# Desde el directorio blacklist-service
PYTHONPATH=. python src/app.py
```

**Opción 2: Usando el punto de entrada de AWS**

```bash
# Desde el directorio blacklist-service
PYTHONPATH=. python application.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Verificar que funciona

```bash
curl http://localhost:5000/health
```

Respuesta esperada: `{"status": "ok"}`

## 🚀 Despliegue en AWS Elastic Beanstalk

### Archivos de configuración incluidos

1. **`.ebextensions/flask.config`** - Configuración WSGI y variables de entorno
2. **`.ebextensions/db-migrate.config`** - Inicialización automática de BD
3. **`application.py`** - Punto de entrada para AWS EB
4. **`.ebignore`** - Archivos a excluir del despliegue

### Crear archivo ZIP para despliegue

```bash
cd blacklist-service
zip -r blacklist-app.zip . -x "*.git*" "__pycache__/*" "*.pyc" ".DS_Store" ".coverage" "test/*" "instance/*"
```

## 📡 API Endpoints

### Base URL

```
http://localhost:5000
```

### Autenticación

Todos los endpoints (excepto `/health`) requieren el header:

```
Authorization: Bearer BearerToken123
```

### Endpoints disponibles

#### 1. Health Check

```http
GET /health
```

**Respuesta:**

```json
{
  "status": "ok"
}
```

#### 2. Agregar Email a Blacklist

```http
POST /blacklists
Content-Type: application/json
Authorization: Bearer BearerToken123
```

**Body:**

```json
{
  "email": "spam@example.com",
  "app_uuid": "12345-app-uuid",
  "blocked_reason": "Sending spam emails"
}
```

**Respuesta exitosa (201):**

```json
{
  "id": 1,
  "email": "spam@example.com",
  "app_uuid": "12345-app-uuid",
  "blocked_reason": "Sending spam emails",
  "ip_address": "127.0.0.1",
  "created_at": "2025-10-13T00:00:00"
}
```

#### 3. Verificar Email en Blacklist

```http
GET /blacklists/{email}
Authorization: Bearer BearerToken123
```

**Respuesta - Email encontrado (200):**

```json
{
  "blacklisted": true,
  "entry": {
    "id": 1,
    "email": "spam@example.com",
    "app_uuid": "12345-app-uuid",
    "blocked_reason": "Sending spam emails",
    "ip_address": "127.0.0.1",
    "created_at": "2025-10-13T00:00:00"
  }
}
```

**Respuesta - Email no encontrado (200):**

```json
{
  "blacklisted": false
}
```

### Códigos de respuesta

| Código | Descripción                    |
| ------ | ------------------------------ |
| 200    | Operación exitosa              |
| 201    | Recurso creado exitosamente    |
| 400    | Error en datos de entrada      |
| 401    | No autorizado (token inválido) |
| 500    | Error interno del servidor     |

### Errores comunes

**401 - No autorizado:**

```json
{
  "error": "Unauthorized"
}
```

**400 - Campos faltantes:**

```json
{
  "error": "Missing required fields"
}
```

**400 - Email duplicado:**

```json
{
  "error": "Email already exists or database error"
}
```

## 🧪 Testing

### Ejecutar todos los tests

```bash
python -m pytest
```

### Ejecutar tests con cobertura

```bash
python -m pytest --cov=src --cov-report=term-missing
```

### Ejecutar tests específicos

```bash
# Tests de GET
python -m pytest test/test_blacklist_get.py -v

# Tests de POST
python -m pytest test/test_blacklist_post.py -v

# Tests de casos de error
python -m pytest test/test_error_cases.py -v
```

### Cobertura actual

- **Cobertura total**: 99%
- **Tests implementados**: 8
- **Casos cubiertos**: Casos exitosos, errores de autenticación, validación, duplicados

## 📮 Postman Collection

### Importar colección

1. Abrir Postman
2. Click en "Import"
3. Seleccionar `Blacklist_API_Postman_Collection.json`
4. La colección incluye:
   - Variables configuradas (`baseUrl`, `bearerToken`)
   - Todos los endpoints con ejemplos
   - Casos de prueba de errores

### Orden recomendado de pruebas

1. Health Check
2. Add Email to Blacklist
3. Check Email in Blacklist - Found
4. Check Email in Blacklist - Not Found
5. Casos de error (401, 400, duplicados)

## 🗄️ Base de Datos

### Modelo de datos

**Tabla: blacklist_entries**

| Campo          | Tipo            | Descripción           |
| -------------- | --------------- | --------------------- |
| id             | Integer (PK)    | Identificador único   |
| email          | String (Unique) | Email en blacklist    |
| app_uuid       | String          | UUID de la aplicación |
| blocked_reason | String          | Razón del bloqueo     |
| ip_address     | String          | IP de quien agregó    |
| created_at     | DateTime        | Fecha de creación     |

### Configuración de base de datos

**SQLite (desarrollo):**

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
```

**PostgreSQL (producción):**

```python
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@host:port/database"
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit los cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

### Estándares de código

- Seguir PEP 8 para Python
- Mantener cobertura de tests > 70%
- Documentar nuevos endpoints en el README
- Agregar tests para nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🔗 Enlaces útiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)

---

**¿Tienes preguntas?** Abre un issue en el repositorio o contacta al equipo de desarrollo.
