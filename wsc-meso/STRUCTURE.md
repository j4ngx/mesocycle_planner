# Mesocycle Planner - Server Structure

Este directorio contiene el servidor FastAPI con arquitectura hexagonal integrada.

## Estructura

```
wsc-meso/
├── src/openapi_server/     # Código autogenerado (NO MODIFICAR)
├── domain/                 # Arquitectura hexagonal - Dominio
├── application/            # Arquitectura hexagonal - Aplicación  
├── infrastructure/         # Arquitectura hexagonal - Infraestructura
├── api/                    # Arquitectura hexagonal - API
├── tests/                  # Tests autogenerados
└── README.md              # Documentación completa
```

## Quick Start

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar MongoDB
brew services start mongodb-community

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Ejecutar servidor
PYTHONPATH=src:. uvicorn src.openapi_server.main:app --reload
```

Ver [README.md](README.md) para documentación completa.
