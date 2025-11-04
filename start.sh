#!/bin/bash
# Script de inicio para Render.com

echo "🌿 Iniciando {DATAR} en Render.com..."

# Verificar que las variables de entorno estén configuradas
if [ -z "$GOOGLE_GENAI_API_KEY" ]; then
    echo "❌ Error: GOOGLE_GENAI_API_KEY no está configurada"
    exit 1
fi

echo "✅ Variables de entorno configuradas"

# Iniciar el servidor
echo "🚀 Iniciando servidor FastAPI..."
cd /opt/render/project/src
uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8080}
