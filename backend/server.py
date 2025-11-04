"""
Servidor Principal FastAPI para el Proyecto {DATAR}
Laboratorio de experimentación con datos ambientales basados en la orquestación de agentes autónomos
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar el orquestador
from orchestrator.agent_orchestrator import get_orchestrator

# Crear aplicación FastAPI
app = FastAPI(
    title="{DATAR} - Laboratorio de Experimentación con Datos Ambientales",
    description="Sistema de orquestación de agentes autónomos para exploración de datos ambientales de Bogotá",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos (frontend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Modelos Pydantic para requests/responses
class MensajeRequest(BaseModel):
    """Modelo para enviar mensajes a los agentes"""
    mensaje: str
    agente_id: Optional[str] = None

class AgenteSelecionRequest(BaseModel):
    """Modelo para seleccionar un agente"""
    agente_id: str

class MensajeResponse(BaseModel):
    """Modelo de respuesta de un agente"""
    exitoso: bool
    agente: Optional[str] = None
    agente_id: Optional[str] = None
    mensaje: Optional[str] = None
    color: Optional[str] = None
    error: Optional[str] = None

class AgenteInfo(BaseModel):
    """Información de un agente"""
    id: str
    nombre: str
    descripcion: str
    color: str

# Obtener instancia del orquestador
orchestrator = get_orchestrator()

# ===== ENDPOINTS =====

@app.get("/", tags=["Info"])
async def root():
    """Redirige automáticamente al frontend de la aplicación"""
    return RedirectResponse(url="/static/index.html")

@app.get("/api/info", tags=["Info"])
async def api_info():
    """Endpoint con información del sistema"""
    return {
        "proyecto": "{DATAR} - Laboratorio de Experimentación con Datos Ambientales",
        "version": "1.0.0",
        "descripcion": "Sistema de orquestación de agentes autónomos impulsados por LLMs",
        "endpoints": {
            "info": "/api/info",
            "agentes_disponibles": "/api/agentes",
            "seleccionar_agente": "/api/agente/seleccionar",
            "enviar_mensaje": "/api/mensaje",
            "historial": "/api/historial",
            "limpiar_historial": "/api/historial/limpiar",
            "documentacion": "/docs",
        },
        "frontend": "/static/index.html"
    }

@app.get("/api/agentes", response_model=List[AgenteInfo], tags=["Agentes"])
async def obtener_agentes():
    """
    Obtiene la lista de todos los agentes disponibles en el sistema

    Retorna información sobre cada agente incluyendo:
    - ID único
    - Nombre descriptivo
    - Descripción de sus capacidades
    - Color asociado para la UI
    """
    try:
        agentes = orchestrator.obtener_lista_agentes()
        return agentes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener agentes: {str(e)}")

@app.post("/api/agente/seleccionar", tags=["Agentes"])
async def seleccionar_agente(request: AgenteSelecionRequest):
    """
    Selecciona un agente específico para interactuar con él

    - **agente_id**: ID del agente a seleccionar (ej: "pasto_bogotano", "susurro_paramo")

    El agente seleccionado quedará activo para las siguientes conversaciones
    hasta que se seleccione otro agente o se limpie el historial.
    """
    try:
        resultado = orchestrator.seleccionar_agente(request.agente_id)
        if not resultado.get("exitoso"):
            raise HTTPException(status_code=404, detail=resultado.get("error"))
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al seleccionar agente: {str(e)}")

@app.post("/api/mensaje", response_model=MensajeResponse, tags=["Interacción"])
async def enviar_mensaje(request: MensajeRequest):
    """
    Envía un mensaje al agente seleccionado o a un agente específico

    - **mensaje**: Texto del mensaje a enviar
    - **agente_id** (opcional): ID del agente específico. Si no se proporciona,
      se usará el agente actualmente seleccionado.

    El agente procesará el mensaje según su especialidad y retornará una respuesta.
    """
    try:
        if not request.mensaje or not request.mensaje.strip():
            raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

        respuesta = await orchestrator.procesar_mensaje(
            mensaje=request.mensaje,
            agente_id=request.agente_id
        )

        if not respuesta.get("exitoso"):
            raise HTTPException(status_code=400, detail=respuesta.get("error"))

        return respuesta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar mensaje: {str(e)}")

@app.get("/api/historial", tags=["Interacción"])
async def obtener_historial():
    """
    Obtiene el historial completo de conversaciones con los agentes

    Retorna una lista con todas las interacciones, incluyendo:
    - Agente que participó
    - Mensaje del usuario
    - Respuesta del agente
    """
    try:
        historial = orchestrator.obtener_historial()
        return {"historial": historial}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")

@app.delete("/api/historial/limpiar", tags=["Interacción"])
async def limpiar_historial():
    """
    Limpia el historial de conversaciones y reinicia el estado del sistema

    Esto resetea:
    - El historial de mensajes
    - La selección del agente activo
    - Cualquier estado interno de las conversaciones
    """
    try:
        orchestrator.limpiar_historial()
        return {"mensaje": "Historial limpiado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al limpiar historial: {str(e)}")

@app.get("/health", tags=["Info"])
async def health_check():
    """Verificar que el servidor está funcionando correctamente"""
    return {
        "status": "OK",
        "servicio": "{DATAR} Backend",
        "agentes_disponibles": len(orchestrator.obtener_lista_agentes())
    }

# ===== EXPERIENCIAS GUIADAS =====

@app.get("/api/experiencias", tags=["Experiencias Guiadas"])
async def obtener_experiencias():
    """
    Obtiene las experiencias guiadas disponibles

    Las experiencias guiadas son flujos predefinidos que combinan varios agentes
    en una secuencia específica para lograr una exploración completa.
    """
    experiencias = [
        {
            "id": "exploracion_sensorial",
            "nombre": "Exploración Sensorial",
            "descripcion": "Un viaje desde la observación hasta la sonificación del territorio",
            "etapas": [
                {"orden": 1, "agente": "bosque", "descripcion": "Observación de especies"},
                {"orden": 2, "agente": "guatilaM", "descripcion": "Interpretación de datos"},
                {"orden": 3, "agente": "pasto_bogotano", "descripcion": "Creación de paisaje sonoro"}
            ],
            "duracion_estimada": "15-20 minutos"
        },
        {
            "id": "narrativa_territorial",
            "nombre": "Narrativa Territorial",
            "descripcion": "Transforma tu experiencia en el territorio en una leyenda futurista",
            "etapas": [
                {"orden": 1, "agente": "susurro_paramo", "descripcion": "Recolección de memoria territorial"},
                {"orden": 2, "agente": "diario_intuitivo", "descripcion": "Visualización emocional"},
            ],
            "duracion_estimada": "10-15 minutos"
        },
        {
            "id": "experimentacion_libre",
            "nombre": "Experimentación Libre",
            "descripcion": "Explora libremente con cualquier combinación de agentes",
            "etapas": [],
            "duracion_estimada": "Variable"
        }
    ]
    return {"experiencias": experiencias}

# ===== INICIALIZACIÓN =====

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 80)
    print("🌿 {DATAR} - Laboratorio de Experimentación con Datos Ambientales")
    print("=" * 80)
    print("📍 Servidor iniciado en: http://localhost:8080")
    print("📍 Documentación API: http://localhost:8080/docs")
    print("📍 Frontend: http://localhost:8080/static/index.html")
    print("=" * 80)
    print(f"🤖 Agentes disponibles: {len(orchestrator.obtener_lista_agentes())}")
    for agente in orchestrator.obtener_lista_agentes():
        print(f"   • {agente['nombre']}: {agente['descripcion']}")
    print("=" * 80 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8080)
