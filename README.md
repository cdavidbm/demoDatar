# 🌿 {DATAR} - Laboratorio de Experimentación con Datos Ambientales

Sistema de experimentación con datos ambientales abiertos basado en la orquestación de agentes autónomos impulsados por modelos de lenguaje (LLMs).

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 🌍 Introducción

El laboratorio **{DATAR}** desarrolla una experimentación transdisciplinar con **datos ambientales abiertos**, utilizando **agentes autónomos impulsados por LLMs**. El proceso busca generar una comprensión más situada y vivencial de la **Estructura Ecológica Principal (EEP)** de Bogotá, combinando trabajo de campo, programación colaborativa y encuentros con expertos en ciencia de datos, ecología y tecnología.

### Objetivos

#### Objetivo General
Diseñar y desarrollar colaborativamente un sistema de experimentación con datos ambientales abiertos, **orquestado por agentes autónomos**, que posibilite una comprensión situada de la Estructura Ecológica Principal de Bogotá.

#### Objetivos Específicos
- Experimentar con los datos ambientales abiertos nuevas formas de aproximarse a los ecosistemas urbanos
- Diseñar e implementar un sistema de experimentación orquestado por agentes autónomos impulsados por LLMs
- Desarrollar una aplicación web que conecte a los usuarios con los datos ambientales abiertos de la ciudad

---

## ✨ Características

- 🤖 **6 Agentes Autónomos Especializados**: Cada uno con personalidad y capacidades únicas
- 🎭 **Orquestación Inteligente**: Sistema que coordina la interacción entre múltiples agentes
- 🌐 **API REST Completa**: Endpoints documentados para todas las funcionalidades
- 📱 **Frontend Responsive**: Diseño mobile-first con HTML, CSS y JavaScript vanilla
- 🎨 **Experiencias Guiadas**: Flujos predefinidos que combinan varios agentes
- 🔊 **Generación de Audio**: Paisajes sonoros algorítmicos con pydub
- 🖼️ **Visualización de Emociones**: Generación de imágenes con NumPy y Pillow
- 🌿 **Conexión con iNaturalist**: Datos reales de biodiversidad de Bogotá
- 📚 **Base de Conocimiento**: Integración con recursos filosóficos y ecológicos

---

## 🏗️ Arquitectura

```
{DATAR}
├── Backend (Python + FastAPI)
│   ├── API iNaturalist
│   ├── Servidor Principal
│   ├── Orquestador de Agentes
│   └── 6 Agentes ADK
│       ├── PastoBogotano
│       ├── Susurro del Páramo
│       ├── GuatilaM
│       ├── Diario Intuitivo
│       ├── Agente Bosque
│       └── Agente Multi-Modal
└── Frontend (HTML + CSS + JS)
    ├── Exploración Libre
    └── Experiencias Guiadas
```

### Tecnologías Utilizadas

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **LLMs**: Google Gemini (ADK Agent Development Kit)
- **Audio**: pydub, sounddevice, FFmpeg
- **Imágenes**: Pillow, NumPy, matplotlib
- **Datos**: API de iNaturalist, BeautifulSoup
- **MCP**: FastMCP para herramientas del Agente Bosque
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- FFmpeg (para procesamiento de audio)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/PropuestaData.git
cd PropuestaData
```

### Paso 2: Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Instalar FFmpeg

#### Windows (con winget)
```bash
winget install ffmpeg
```

#### macOS (con Homebrew)
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Paso 5: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu GEMINI_API_KEY
nano .env  # o el editor de tu preferencia
```

Obtén tu API Key de Gemini en: https://makersuite.google.com/app/apikey

---

## ⚙️ Configuración

### Variables de Entorno Principales

```env
# Obligatorio
GEMINI_API_KEY=tu_api_key_aqui

# Opcional (con valores por defecto)
SERVER_PORT=8080
SERVER_HOST=0.0.0.0
DEBUG_MODE=development
DEFAULT_MODEL=gemini-2.5-flash
```

### Configuración de Archivos de Audio

Para que el agente **PastoBogotano** funcione correctamente, necesitas archivos de audio:

```bash
# Crear directorio de sonidos
mkdir -p backend/sounds

# Añadir archivos de audio (formato WAV recomendado)
# - bird-bogota.wav
# - insect.wav
# - wind.wav
# - tinguas.wav
```

---

## 🎯 Uso

### Iniciar el Servidor

```bash
# Desde el directorio raíz del proyecto
python backend/server.py
```

El servidor se iniciará en: `http://localhost:8080`

### Acceder a la Aplicación

- **Frontend**: http://localhost:8080/static/index.html
- **API Docs (Swagger)**: http://localhost:8080/docs
- **API Docs (ReDoc)**: http://localhost:8080/redoc

### Modos de Exploración

#### 1. Exploración Libre
- Selecciona uno o más agentes
- Chatea directamente con ellos
- Cada agente responde según su especialidad

#### 2. Experiencias Guiadas
- **Exploración Sensorial**: Bosque → GuatilaM → PastoBogotano
- **Narrativa Territorial**: Susurro del Páramo → Diario Intuitivo
- **Experimentación Libre**: Combina agentes a tu gusto

---

## 🤖 Agentes Disponibles

### 1. 🌿 PastoBogotano
**Creador de Paisajes Sonoros**

- **Especialidad**: Generación de composiciones sonoras algorítmicas
- **Tecnología**: pydub, efectos de audio (eco, inversión, pitch)
- **Personalidad**: Minimalista verbal, expresivo sonoro
- **Output**: Archivos MP3 de 6-20 segundos

### 2. 🌄 Susurro del Páramo
**Oráculo Narrativo-Legendario**

- **Especialidad**: Transformación de experiencias en leyendas futuristas
- **Tecnología**: LLM con temperature 2.0, integración mitología Muisca
- **Personalidad**: Guardián de historias, tono íntimo y sabio
- **Output**: Leyendas de 4 párrafos con especies de iNaturalist

### 3. 🦎 GuatilaM
**Intérprete Dual**

- **Especialidad**: Respuestas en texto + emojis simultáneamente
- **Tecnología**: Arquitectura de agentes paralelos (ParallelAgent + SequentialAgent)
- **Personalidad**: Biocéntrico, valora todas las formas de vida
- **Output**: Texto informativo (~10 frases) + interpretación con emojis

### 4. 🌊 Diario Intuitivo
**Visualizador de Ríos Emocionales**

- **Especialidad**: Traducción de emojis en visualizaciones artísticas
- **Tecnología**: NumPy + Pillow, 5 estilos de trazo según emoción
- **Personalidad**: Intérprete del pensamiento como río
- **Output**: Imágenes PNG con trazos dinámicos

### 5. 🌳 Agente Bosque
**Educador Ecológico**

- **Especialidad**: Despertar curiosidad sobre vida oculta (musgos, líquenes, hongos)
- **Tecnología**: FastMCP con 4 herramientas (inferir_especies, explorar_pdf, etc.)
- **Personalidad**: Curioso, filosóficamente reflexivo
- **Output**: Inferencias de especies + preguntas filosóficas

### 6. 🔬 Agente Multi-Modal
**Conector Sistémico**

- **Especialidad**: Respuestas en 3 formatos alternados (Turtle/ASCII-Morse/NumPy-Audio)
- **Tecnología**: Scripts de visualización y sonido
- **Personalidad**: Visión macro-micro, biocéntrico
- **Output**: Código Python para gráficas, código Morse, o composiciones sonoras

---

## 🔌 API REST

### Endpoints Principales

#### Información del Sistema
```http
GET /
GET /health
```

#### Agentes
```http
GET /api/agentes
POST /api/agente/seleccionar
```

#### Interacción
```http
POST /api/mensaje
GET /api/historial
DELETE /api/historial/limpiar
```

#### Experiencias Guiadas
```http
GET /api/experiencias
```

### Ejemplo de Uso

```python
import requests

# Listar agentes disponibles
response = requests.get('http://localhost:8080/api/agentes')
agentes = response.json()

# Seleccionar un agente
requests.post('http://localhost:8080/api/agente/seleccionar',
    json={"agente_id": "pasto_bogotano"})

# Enviar mensaje
response = requests.post('http://localhost:8080/api/mensaje',
    json={"mensaje": "Crea un paisaje sonoro del amanecer"})
print(response.json())
```

---

## 📂 Estructura del Proyecto

```
PropuestaData/
├── backend/
│   ├── api/
│   │   └── inaturalist_api.py        # API de iNaturalist
│   ├── agents/
│   │   ├── pasto_bogotano/           # Agente 1
│   │   │   └── agent.py
│   │   ├── susurro_paramo/           # Agente 2
│   │   │   └── agent.py
│   │   ├── guatilaM/                 # Agente 3
│   │   │   ├── agent.py
│   │   │   ├── utils.py
│   │   │   └── instrucciones/
│   │   ├── diario_intuitivo/         # Agente 4
│   │   │   ├── agent.py
│   │   │   └── visualizacion.py
│   │   ├── bosque/                   # Agente 5
│   │   │   ├── agent.py
│   │   │   └── mcp_server_bosque.py
│   │   └── multimodal/               # Agente 6
│   │       └── agent.py
│   ├── orchestrator/
│   │   └── agent_orchestrator.py     # Orquestador principal
│   ├── sounds/                       # Archivos de audio
│   ├── output/                       # Audio generado
│   └── server.py                     # Servidor FastAPI
├── frontend/
│   ├── index.html                    # Página principal
│   ├── css/
│   │   └── styles.css                # Estilos responsive
│   └── js/
│       └── app.js                    # Lógica de frontend
├── imagenes_generadas/               # Imágenes del Diario Intuitivo
├── .env.example                      # Plantilla de variables de entorno
├── requirements.txt                  # Dependencias Python
├── README.md                         # Este archivo
└── instrucciones.md                  # Instrucciones originales del proyecto
```

---

## 🤝 Contribuciones

Este proyecto es el resultado del trabajo colaborativo de:

### Participantes

- **pncho-dev**: PastoBogotano (paisajes sonoros)
- **zolsemiya**: Susurro del Páramo (leyendas)
- **GuatilaM**: Sistema GuatilaM (interpretación dual)
- **M4r1l1**: Diario Intuitivo (visualización emocional)
- **LinaPuerto**: Agente Bosque (educación ecológica)
- **Sebastian1022**: Agente Multi-Modal (conexión sistémica)

### Cómo Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

---

## 📜 Metodología

El laboratorio se desarrolla bajo el enfoque de **Research through Design (RtD)**, experimentando con los datos mediante la co-creación de un sistema digital que interactúa con las **API REST** de las plataformas de datos abiertos de Bogotá.

Siguiendo la mirada de **Tim Ingold (2011)**, los datos son interpretados no como puntos fijos en una red, sino como **líneas vivas entrelazadas** que conforman una **malla (meshwork)** de trayectorias y relaciones.

---

## 🌿 Datos Ambientales

**iNaturalist Colombia**

Plataforma de ciencia ciudadana administrada por el Instituto Alexander von Humboldt, donde se registran colaborativamente observaciones de biodiversidad.

- Web: https://colombia.inaturalist.org
- API: https://api.inaturalist.org/v1

---

**{DATAR}** - *Tejiendo datos ambientales con conciencia territorial* 🌿
