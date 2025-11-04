# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**{DATAR}** is a laboratory for environmental data experimentation based on autonomous agent orchestration powered by LLMs. The system coordinates 6 specialized agents that interact with environmental open data from Bogotá (specifically iNaturalist Colombia) to create immersive experiences combining audio, text, emojis, visualizations, and narratives.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Running the Application
```bash
# Start main server (from project root)
python backend/server.py

# Server runs on http://localhost:8080
# Frontend: http://localhost:8080/static/index.html
# API Docs: http://localhost:8080/docs
```

### Running Individual Components
```bash
# Run iNaturalist API standalone
python backend/api/inaturalist_api.py

# Run MCP server for Agente Bosque (testing)
python backend/agents/bosque/mcp_server_bosque.py
```

## Architecture & Design Patterns

### Agent Orchestration Pattern

The system uses a **centralized orchestrator** (`backend/orchestrator/agent_orchestrator.py`) that:
1. Maintains a registry of all 6 agents with metadata (name, description, color)
2. Routes user messages to the selected agent
3. Manages conversation history
4. Provides a singleton instance via `get_orchestrator()`

**Key architectural decision**: Agent instances are stored as `None` in the AGENTES dictionary and initialized dynamically to avoid circular imports and heavy initialization on startup.

### Agent Specializations

Each agent in `backend/agents/` has a distinct purpose and technology stack:

1. **pasto_bogotano**: Audio generation using pydub
   - Generates algorithmic soundscapes (6-20 sec MP3)
   - Applies effects: echo, reversal, pitch shifting
   - Requires WAV files in `backend/sounds/`

2. **susurro_paramo**: Narrative generation with high temperature (2.0)
   - Uses iNaturalist API to fetch species
   - Integrates Muisca mythology
   - Implements "inverted ending" logic based on user emotions

3. **guatilaM**: Parallel + Sequential agent architecture
   - Uses ADK's `ParallelAgent` to run `normal_agent` + `emoji_agent` simultaneously
   - Uses `SequentialAgent` to merge responses via `merger_agent`
   - Reads instructions from `instrucciones/*.txt` files

4. **diario_intuitivo**: Two-step emotional visualization
   - Step 1: User sends emojis → agent interprets and saves to global `_ultima_interpretacion`
   - Step 2: User says "imagen" → generates PNG using NumPy/Pillow based on saved interpretation
   - **Critical**: Must call `guardar_interpretacion_emocional()` before responding to user

5. **bosque**: MCP-based knowledge retrieval
   - Uses FastMCP server (`mcp_server_bosque.py`) with 4 tools:
     - `inferir_especies`: Maps environmental conditions to species
     - `explorar_pdf`: Generates philosophical questions (hardcoded responses, not actual PDFs)
     - `explorar`: Web scraping
     - `leer_pagina`: Web page fetching
   - Three-stage conversational flow: observation → inference → philosophical deepening

6. **multimodal**: Rotating output formats
   - Alternates responses between Turtle code, ASCII/Morse, and NumPy audio
   - Temperature: 0.8

### Frontend Architecture

**Single-page application** (`frontend/index.html`) with two modes:

1. **Free Exploration Mode** (`#free-mode`)
   - Renders agent cards from `/api/agentes`
   - Opens chat on agent selection
   - Sends messages to `/api/mensaje`

2. **Guided Experiences Mode** (`#guided-mode`)
   - Loads predefined journeys from `/api/experiencias`
   - Manages multi-stage flows with progress tracking
   - Three experiences defined in `server.py`:
     - Exploración Sensorial (3 stages: bosque → guatilaM → pasto_bogotano)
     - Narrativa Territorial (2 stages: susurro_paramo → diario_intuitivo)
     - Experimentación Libre (no stages)

**State management** in `frontend/js/app.js`:
- `selectedAgent`: Currently active agent
- `currentExperience`: Active guided experience
- `currentStage`: Current step in guided flow

### API Design

REST API follows this pattern:
- `/api/agentes` - GET: List all agents
- `/api/agente/seleccionar` - POST: Set active agent
- `/api/mensaje` - POST: Send message to agent
- `/api/historial` - GET: Retrieve conversation history
- `/api/experiencias` - GET: List guided experiences

**Important**: The orchestrator maintains stateful conversation history. Use `/api/historial/limpiar` (DELETE) to reset state between sessions.

## Critical Integration Points

### ADK Agent Initialization
All agents use `from google.adk.agents.llm_agent import Agent`. The ADK library may require special installation:
```bash
pip install git+https://github.com/google/adk-toolkit.git
```

### Environment Variables Required
- `GEMINI_API_KEY`: **Mandatory** for all LLM agents
- `SOUNDS_DIR`, `OUTPUT_DIR`: Optional, default paths exist

### File System Dependencies
- `backend/sounds/*.wav`: Required for pasto_bogotano (bird-bogota, insect, wind, tinguas)
- `backend/agents/guatilaM/instrucciones/*.txt`: Required for GuatilaM agent logic
- `imagenes_generadas/`: Auto-created for diario_intuitivo output

### Cross-Origin Resource Sharing
Frontend makes requests from `http://localhost:8080/static/` to `http://localhost:8080/api/`. CORS is configured in `server.py` to allow all origins (`allow_origins=["*"]`). **In production**, restrict to specific domains.

## Agent Development Guidelines

### Adding a New Agent

1. Create directory: `backend/agents/new_agent/`
2. Create `agent.py` with `root_agent = Agent(...)` export
3. Add entry to `AGENTES` dict in `orchestrator/agent_orchestrator.py`
4. Import in orchestrator try/except block
5. Add metadata (nombre, descripcion, color) to AGENTES
6. Update frontend `getAgentIcon()` in `app.js` if custom icon needed

### Agent Tool Development

Tools are Python functions passed to `Agent(tools=[...])`:
- Must have clear docstrings (ADK uses them for LLM context)
- Return type should be `str` (displayed to user)
- For async operations, use `async def`
- Errors should return descriptive messages, not raise exceptions

### MCP Server Pattern (Agente Bosque)

If agent needs external knowledge/tools:
1. Create `mcp_server_*.py` with `FastMCP("server_name")`
2. Define tools with `@mcp.tool()` decorator
3. Connect in agent: `MCPToolset(connection_params=StdioConnectionParams(...))`
4. Run server as subprocess via StdioServerParameters

## Frontend Development

### Modifying UI
- CSS: `frontend/css/styles.css` uses CSS custom properties (variables) for theming
- Color scheme defined in `:root` - modify there for global changes
- Mobile-first: Base styles for mobile, `@media` queries for tablet (768px) and desktop (1024px)

### Adding API Endpoints
1. Define Pydantic models in `server.py` (MensajeRequest, etc.)
2. Create async endpoint function with FastAPI decorators
3. Use `orchestrator` singleton: `orchestrator = get_orchestrator()`
4. Update OpenAPI docs with descriptive docstrings
5. Add to `frontend/js/app.js` API calls using fetch()

## Testing Considerations

**No test suite currently exists**. When implementing:
- Mock ADK agents (they require API keys)
- Mock iNaturalist API responses (use fixtures)
- Test orchestrator routing logic independently
- Test frontend with local backend mock server

## Common Issues

### Import Errors on Startup
If agents fail to import, server continues but agents are unavailable. Check:
- Virtual environment activated
- All requirements installed
- `GEMINI_API_KEY` in .env
- Python path includes `backend/`

### Audio Generation Fails
PastoBogotano requires:
- FFmpeg installed system-wide
- WAV files in `backend/sounds/` matching exact names in `ARCHIVOS_SONIDOS`
- Write permissions to `backend/output/`

### MCP Server Not Responding
Agente Bosque's MCP server runs as subprocess:
- Check `python` command is in PATH
- Verify `mcp_server_bosque.py` path is correct
- Server logs to stdout (check terminal output)

### Frontend Not Loading
- Ensure `frontend/` directory exists relative to `server.py`
- StaticFiles mount only happens if path exists
- Check browser console for CORS errors

## Project Context

This is a collaborative project where each of 6 participants developed one agent independently. The orchestrator integrates all work while preserving each participant's unique implementation. When modifying agents, maintain the original contributor's style and approach.
