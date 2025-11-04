"""
Agente Orquestador para el Proyecto {DATAR}
Coordina la interacción entre los diferentes agentes del sistema
"""

import sys
import os

# Agregar el directorio padre al path para importar los agentes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List, Any
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, Content

# Importar los agentes individuales
try:
    from agents.pasto_bogotano.agent import root_agent as pasto_bogotano_agent
    from agents.susurro_paramo.agent import root_agent as susurro_paramo_agent
    from agents.guatilaM.agent import root_agent as guatilaM_agent
    from agents.diario_intuitivo.agent import root_agent as diario_intuitivo_agent
    from agents.bosque.agent import root_agent as bosque_agent
    from agents.multimodal.agent import root_agent as multimodal_agent
except ImportError as e:
    print(f"⚠️ Error al importar agentes: {e}")
    print("Algunos agentes pueden no estar disponibles.")

# Diccionario de agentes disponibles
AGENTES = {
    "pasto_bogotano": {
        "nombre": "PastoBogotano",
        "descripcion": "Crea paisajes sonoros de Bogotá",
        "agente": pasto_bogotano_agent,
        "color": "#90EE90"
    },
    "susurro_paramo": {
        "nombre": "Susurro del Páramo",
        "descripcion": "Teje leyendas desde tu experiencia territorial",
        "agente": susurro_paramo_agent,
        "color": "#87CEEB"
    },
    "guatilaM": {
        "nombre": "GuatilaM",
        "descripcion": "Interpreta datos ambientales en texto y emojis",
        "agente": guatilaM_agent,
        "color": "#FFD700"
    },
    "diario_intuitivo": {
        "nombre": "Diario Intuitivo",
        "descripcion": "Visualiza ríos emocionales desde emojis",
        "agente": diario_intuitivo_agent,
        "color": "#FF69B4"
    },
    "bosque": {
        "nombre": "Agente Bosque",
        "descripcion": "Descubre la vida oculta del bosque",
        "agente": bosque_agent,
        "color": "#228B22"
    },
    "multimodal": {
        "nombre": "Agente Multi-Modal",
        "descripcion": "Conecta lo macro y lo micro de manera sistémica",
        "agente": multimodal_agent,
        "color": "#9370DB"
    }
}

class OrchestrationAgent:
    """
    Agente orquestador que coordina la interacción entre múltiples agentes
    """

    def __init__(self):
        """Inicializa el orquestador con los agentes disponibles"""
        self.agentes = AGENTES
        self.agente_activo = None
        self.historial_conversacion = []

        # Crear runners para cada agente
        self.runners = {}
        self.sessions = {}  # sesiones por agente
        for agente_id, agente_info in self.agentes.items():
            if agente_info["agente"] is not None:
                try:
                    self.runners[agente_id] = InMemoryRunner(agent=agente_info["agente"])
                except Exception as e:
                    print(f"⚠️ Error al crear runner para {agente_id}: {e}")

    def obtener_lista_agentes(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de agentes disponibles con su información
        """
        return [
            {
                "id": key,
                "nombre": value["nombre"],
                "descripcion": value["descripcion"],
                "color": value["color"]
            }
            for key, value in self.agentes.items()
        ]

    def seleccionar_agente(self, agente_id: str) -> Dict[str, Any]:
        """
        Selecciona un agente por su ID

        Args:
            agente_id: ID del agente a seleccionar

        Returns:
            Diccionario con información sobre el agente seleccionado
        """
        if agente_id not in self.agentes:
            return {
                "exitoso": False,
                "error": f"Agente '{agente_id}' no encontrado"
            }

        self.agente_activo = agente_id
        agente_info = self.agentes[agente_id]

        return {
            "exitoso": True,
            "agente": agente_info["nombre"],
            "descripcion": agente_info["descripcion"],
            "mensaje": f"Has seleccionado a {agente_info['nombre']}. ¿Qué quieres explorar?"
        }

    async def procesar_mensaje(self, mensaje: str, agente_id: str = None) -> Dict[str, Any]:
        """
        Procesa un mensaje y lo enruta al agente apropiado

        Args:
            mensaje: Mensaje del usuario
            agente_id: ID del agente específico (opcional)

        Returns:
            Respuesta del agente con metadata
        """
        try:
            # Determinar qué agente usar
            if agente_id:
                target_agent = agente_id
            elif self.agente_activo:
                target_agent = self.agente_activo
            else:
                return {
                    "exitoso": False,
                    "error": "No hay ningún agente seleccionado. Por favor, selecciona un agente primero."
                }

            if target_agent not in self.agentes:
                return {
                    "exitoso": False,
                    "error": f"Agente '{target_agent}' no encontrado"
                }

            # Verificar que el runner existe
            if target_agent not in self.runners:
                return {
                    "exitoso": False,
                    "error": f"Agente '{target_agent}' no está disponible"
                }

            # Obtener el agente y runner
            agente_info = self.agentes[target_agent]
            runner = self.runners[target_agent]

            # Crear o recuperar sesión para este agente
            if target_agent not in self.sessions:
                self.sessions[target_agent] = await runner.session_service.create_session(
                    app_name=runner.app_name,
                    user_id="default_user"
                )

            session = self.sessions[target_agent]

            # Crear el contenido del mensaje
            content = Content(parts=[Part(text=mensaje)], role="user")

            # Ejecutar el agente y recolectar la respuesta
            respuesta_texto = ""
            for event in runner.run(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content
            ):
                # Extraer el texto de la respuesta
                if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            respuesta_texto += part.text

            # Si no hay respuesta, usar un mensaje por defecto
            if not respuesta_texto:
                respuesta_texto = f"[{agente_info['nombre']}] procesó tu mensaje, pero no generó una respuesta de texto."

            respuesta = {
                "exitoso": True,
                "agente": agente_info["nombre"],
                "agente_id": target_agent,
                "mensaje": respuesta_texto,
                "color": agente_info["color"]
            }

            # Guardar en historial
            self.historial_conversacion.append({
                "agente": target_agent,
                "usuario": mensaje,
                "respuesta": respuesta_texto
            })

            return respuesta

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ Error detallado al procesar mensaje: {error_detail}")
            return {
                "exitoso": False,
                "error": f"Error al procesar mensaje: {str(e)}"
            }

    def obtener_historial(self) -> List[Dict[str, Any]]:
        """Retorna el historial de conversaciones"""
        return self.historial_conversacion

    def limpiar_historial(self):
        """Limpia el historial de conversaciones y sesiones"""
        self.historial_conversacion = []
        self.agente_activo = None
        # Limpiar las sesiones para reiniciar las conversaciones
        self.sessions = {}

# Crear instancia global del orquestador
orchestrator = OrchestrationAgent()

def get_orchestrator() -> OrchestrationAgent:
    """Retorna la instancia del orquestador"""
    return orchestrator
