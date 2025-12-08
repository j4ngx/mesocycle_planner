# Mesocycle Planner API - Hexagonal Architecture

Implementación de arquitectura hexagonal estricta integrada con el código autogenerado de FastAPI en el directorio `wsc-meso/`.

## 📁 Estructura del Proyecto

```
wsc-meso/
├── src/openapi_server/        # 🤖 Código autogenerado por OpenAPI Generator
│   ├── main.py                # FastAPI app con rutas autogeneradas
│   ├── apis/                  # API handlers autogenerados
│   ├── models/                # Modelos Pydantic autogenerados
│   └── security_api.py        # Seguridad autogenerada
│
├── domain/                    # ✅ Capa de Dominio (sin dependencias externas)
│   ├── entities/              # Entidades de dominio
│   │   ├── user.py           # Usuario con autenticación
│   │   ├── exercise.py       # Ejercicio con datos biomecánicos
│   │   ├── mesocycle.py      # Mesociclo con periodización
│   │   ├── microcycle.py     # Microciclo con fases de entrenamiento
│   │   ├── workout.py        # Entrenamiento
│   │   ├── training_session.py  # Sesión de entrenamiento con métricas
│   │   └── progress.py       # Progreso del usuario
│   └── repositories/          # Interfaces de repositorios (puertos)
│       ├── user_repository.py
│       ├── exercise_repository.py
│       ├── mesocycle_repository.py
│       ├── workout_repository.py
│       └── progress_repository.py
│
├── application/               # Capa de Aplicación (casos de uso)
│   ├── use_cases/            # Casos de uso de la aplicación
│   ├── dtos/                 # Data Transfer Objects
│   └── services/             # Servicios de aplicación
│
├── infrastructure/            # Capa de Infraestructura (implementaciones)
│   ├── config/               # Configuración
│   │   ├── database.py      # Configuración de MongoDB
│   │   └── settings.py      # Settings de la aplicación
│   └── persistence/          # Persistencia
│       ├── models/           # Modelos de MongoDB
│       │   ├── user_model.py
│       │   ├── exercise_model.py
│       │   ├── mesocycle_model.py
│       │   ├── workout_model.py
│       │   └── progress_model.py
│       └── repositories/     # Implementaciones de repositorios
│           ├── user_repository_impl.py
│           └── mesocycle_repository_impl.py
│
└── api/                      # Capa API (HTTP)
    ├── controllers/          # Controladores HTTP
    ├── dependencies/         # Inyección de dependencias
    ├── middleware/           # Middleware
    └── schemas/              # Schemas de request/response

```

## 🏗️ Arquitectura Hexagonal

### Principios

1. **Dominio** (núcleo): Lógica de negocio pura, sin dependencias externas
2. **Aplicación**: Orquestación de casos de uso
3. **Infraestructura**: Implementaciones concretas (MongoDB, etc.)
4. **API**: Interfaz HTTP con FastAPI

### Flujo de Dependencias

```
API → Application → Domain ← Infrastructure
```

- Las capas externas dependen de las internas
- El dominio no conoce la infraestructura
- Los repositorios son interfaces (puertos) en el dominio
- Las implementaciones (adaptadores) están en infraestructura

## 🚀 Características Implementadas

### Dominio

- ✅ **Entidades** con lógica de negocio y validaciones
- ✅ **Value Objects** (IntensityRange, SetPerformed, etc.)
- ✅ **Repository Interfaces** (puertos)
- ✅ **Reglas de negocio** encapsuladas en entidades

### Infraestructura

- ✅ **MongoDB** con Motor (driver async)
- ✅ **Modelos Pydantic** para validación
- ✅ **Implementaciones de repositorios**
- ✅ **Configuración** centralizada
- ✅ **Índices de base de datos** para rendimiento

## 📦 Dependencias

```bash
# Core
fastapi>=0.115.0
uvicorn>=0.13.4
pydantic>=2.0
pydantic-settings>=2.0

# Database
motor>=3.3.0  # MongoDB async driver
pymongo>=4.5.0

# Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

# Utilities
python-dotenv>=0.17.1
```

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz:

```env
# Application
APP_NAME=Mesocycle Planner API
DEBUG=False

# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=mesocycle_planner

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

## 🗄️ MongoDB Setup

### Instalación Local

```bash
# macOS
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Verificar
mongosh
```

### Docker

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest
```

## 🏃 Ejecución

### Desarrollo

```bash
# Navegar al directorio del servidor
cd wsc-meso

# Crear entorno virtual (si no existe)
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias (incluye las de arquitectura hexagonal)
pip install -r requirements.txt

# Ejecutar servidor
PYTHONPATH=src:. uvicorn src.openapi_server.main:app --reload --host 0.0.0.0 --port 8000
```

### Acceder a la documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Unit tests (dominio)
pytest tests/unit/

# Integration tests (repositorios)
pytest tests/integration/

# E2E tests (API)
pytest tests/e2e/
```

## 📝 Ejemplos de Uso

### Crear Usuario

```python
from domain.entities.user import User, TrainingLevel

user = User.create(
    email="athlete@example.com",
    username="athlete123",
    hashed_password="$2b$12$...",
    full_name="John Doe",
    training_level=TrainingLevel.INTERMEDIATE
)
```

### Crear Mesociclo

```python
from domain.entities.mesocycle import Mesocycle, PeriodizationModel, TrainingGoal
from datetime import date
from uuid import uuid4

mesocycle = Mesocycle.create(
    user_id=uuid4(),
    name="12w Hypertrophy DUP",
    periodization_model=PeriodizationModel.DAILY_UNDULATING,
    goal=TrainingGoal.HYPERTROPHY,
    duration_weeks=12,
    start_date=date(2025, 1, 1),
    end_date=date(2025, 3, 24),
    training_level="intermediate",
    weekly_frequency=5,
    deload_weeks=[4, 8, 12]
)

# Iniciar mesociclo
mesocycle.start()
```

## 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación:

1. **Register**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login` → Devuelve access_token
3. **Usar token**: Header `Authorization: Bearer {token}`

## 🎯 Próximos Pasos

1. **Completar casos de uso** en la capa de aplicación
2. **Implementar controladores** en la capa API
3. **Configurar inyección de dependencias**
4. **Añadir tests unitarios e integración**
5. **Implementar generación AI de mesociclos**
6. **Añadir tracking de sesiones con métricas**

## 📚 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Motor Documentation](https://motor.readthedocs.io/)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

## 🤝 Integración con Código Autogenerado

El código autogenerado en `wsc-meso/` proporciona:
- Schemas OpenAPI
- Rutas FastAPI base
- Modelos Pydantic de request/response

Este código hexagonal proporciona:
- Lógica de negocio
- Persistencia en MongoDB
- Casos de uso

**Integración**: Los controladores en `api/` conectarán las rutas autogeneradas con los casos de uso de esta arquitectura.
