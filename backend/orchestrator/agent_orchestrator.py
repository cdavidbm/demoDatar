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
        "agente": None,  # Se inicializará dinámicamente
        "color": "#90EE90"
    },
    "susurro_paramo": {
        "nombre": "Susurro del Páramo",
        "descripcion": "Teje leyendas desde tu experiencia territorial",
        "agente": None,
        "color": "#87CEEB"
    },
    "guatilaM": {
        "nombre": "GuatilaM",
        "descripcion": "Interpreta datos ambientales en texto y emojis",
        "agente": None,
        "color": "#FFD700"
    },
    "diario_intuitivo": {
        "nombre": "Diario Intuitivo",
        "descripcion": "Visualiza ríos emocionales desde emojis",
        "agente": None,
        "color": "#FF69B4"
    },
    "bosque": {
        "nombre": "Agente Bosque",
        "descripcion": "Descubre la vida oculta del bosque",
        "agente": None,
        "color": "#228B22"
    },
    "multimodal": {
        "nombre": "Agente Multi-Modal",
        "descripcion": "Conecta lo macro y lo micro de manera sistémica",
        "agente": None,
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

            # Obtener el agente
            agente_info = self.agentes[target_agent]

            # Aquí se procesaría el mensaje con el agente real
            # Por ahora, retornamos una respuesta simulada
            respuesta = {
                "exitoso": True,
                "agente": agente_info["nombre"],
                "agente_id": target_agent,
                "mensaje": f"[{agente_info['nombre']}]: Procesando tu mensaje '{mensaje}'...",
                "color": agente_info["color"]
            }

            # Guardar en historial
            self.historial_conversacion.append({
                "agente": target_agent,
                "usuario": mensaje,
                "respuesta": respuesta["mensaje"]
            })

            return respuesta

        except Exception as e:
            return {
                "exitoso": False,
                "error": f"Error al procesar mensaje: {str(e)}"
            }

    def obtener_historial(self) -> List[Dict[str, Any]]:
        """Retorna el historial de conversaciones"""
        return self.historial_conversacion

    def limpiar_historial(self):
        """Limpia el historial de conversaciones"""
        self.historial_conversacion = []
        self.agente_activo = None

# Crear instancia global del orquestador
orchestrator = OrchestrationAgent()

def get_orchestrator() -> OrchestrationAgent:
    """Retorna la instancia del orquestador"""
    return orchestrator
