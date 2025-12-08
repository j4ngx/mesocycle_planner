#!/bin/bash

# Script para iniciar el backend de Mesocycle Planner
# Asegúrate de que Docker Desktop esté corriendo antes de ejecutar este script

set -e

echo "🚀 Iniciando Mesocycle Planner Backend..."
echo ""

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo"
    echo "Por favor, inicia Docker Desktop y vuelve a ejecutar este script"
    exit 1
fi

echo "✅ Docker está corriendo"
echo ""

# Navegar al directorio del backend
cd "$(dirname "$0")/wsc-meso"

# Iniciar MongoDB con Docker Compose
echo "📦 Iniciando MongoDB..."
docker compose up -d

# Esperar a que MongoDB esté listo
echo "⏳ Esperando a que MongoDB esté listo..."
sleep 5

# Verificar que MongoDB esté corriendo
if docker compose ps | grep -q "Up"; then
    echo "✅ MongoDB está corriendo"
else
    echo "❌ Error: MongoDB no se inició correctamente"
    exit 1
fi

echo ""
echo "🔥 Iniciando servidor FastAPI..."
echo "El servidor estará disponible en: http://localhost:8000"
echo "Documentación API: http://localhost:8000/docs"
echo "Mongo Express: http://localhost:8081"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Activar entorno virtual e iniciar FastAPI
source venv/bin/activate
PYTHONPATH=src:. uvicorn src.openapi_server.main:app --reload --host 0.0.0.0 --port 8000
