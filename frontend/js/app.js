/**
 * {DATAR} - Frontend JavaScript
 * Lógica de interacción con los agentes y experiencias guiadas
 */

// ===== CONFIGURACIÓN =====
const API_BASE_URL = 'http://localhost:8080';
let currentMode = 'free'; // 'free' or 'guided'
let selectedAgent = null;
let agents = [];
let experiences = [];
let currentExperience = null;
let currentStage = 0;

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌿 Iniciando {DATAR}...');

    // Cargar agentes
    await loadAgents();

    // Cargar experiencias
    await loadExperiences();

    // Setup event listeners
    setupEventListeners();

    console.log('✅ Sistema inicializado');
});

// ===== FUNCIONES DE CARGA =====

/**
 * Carga la lista de agentes desde la API
 */
async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/agentes`);
        if (!response.ok) throw new Error('Error al cargar agentes');

        agents = await response.json();
        console.log('Agentes cargados:', agents.length);

        renderAgents();
    } catch (error) {
        console.error('Error al cargar agentes:', error);
        showNotification('Error al cargar agentes. Por favor, verifica que el servidor esté corriendo.', 'error');
    }
}

/**
 * Carga la lista de experiencias guiadas desde la API
 */
async function loadExperiences() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/experiencias`);
        if (!response.ok) throw new Error('Error al cargar experiencias');

        const data = await response.json();
        experiences = data.experiencias;
        console.log('Experiencias cargadas:', experiences.length);

        renderExperiences();
    } catch (error) {
        console.error('Error al cargar experiencias:', error);
        showNotification('Error al cargar experiencias guiadas.', 'error');
    }
}

// ===== FUNCIONES DE RENDERIZADO =====

/**
 * Renderiza las tarjetas de agentes en el grid
 */
function renderAgents() {
    const grid = document.getElementById('agents-grid');
    if (!grid) return;

    grid.innerHTML = agents.map(agent => `
        <div class="agent-card" id="agent-${agent.id}" onclick="selectAgent('${agent.id}')">
            <div class="agent-card__header">
                <div class="agent-card__icon" style="background-color: ${agent.color}">
                    ${getAgentIcon(agent.id)}
                </div>
                <h3 class="agent-card__title">${agent.nombre}</h3>
            </div>
            <p class="agent-card__description">${agent.descripcion}</p>
            <button class="agent-card__button">
                Chatear con ${agent.nombre}
            </button>
        </div>
    `).join('');
}

/**
 * Renderiza las tarjetas de experiencias guiadas
 */
function renderExperiences() {
    const grid = document.getElementById('experiences-grid');
    if (!grid) return;

    grid.innerHTML = experiences.map(exp => `
        <div class="experience-card" onclick="startExperience('${exp.id}')">
            <h3 class="experience-card__title">${exp.nombre}</h3>
            <p class="experience-card__description">${exp.descripcion}</p>
            <div class="experience-card__details">
                <div class="experience-card__stages">
                    ${exp.etapas.map(() => '<span class="stage-dot"></span>').join('')}
                </div>
                <span>${exp.duracion_estimada}</span>
            </div>
        </div>
    `).join('');
}

/**
 * Retorna el icono emoji para cada agente
 */
function getAgentIcon(agentId) {
    const icons = {
        'pasto_bogotano': '🌿',
        'susurro_paramo': '🌄',
        'guatilaM': '🦎',
        'diario_intuitivo': '🌊',
        'bosque': '🌳',
        'multimodal': '🔬'
    };
    return icons[agentId] || '🤖';
}

// ===== FUNCIONES DE MODO =====

/**
 * Cambia entre modo libre y modo guiado
 */
function showMode(mode) {
    currentMode = mode;

    // Update buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    if (mode === 'free') {
        document.querySelector('.mode-btn--free').classList.add('active');
        document.getElementById('free-mode').style.display = 'block';
        document.getElementById('guided-mode').style.display = 'none';
        closeExperience();
    } else {
        document.querySelector('.mode-btn--guided').classList.add('active');
        document.getElementById('free-mode').style.display = 'none';
        document.getElementById('guided-mode').style.display = 'block';
        closeChat();
    }
}

// ===== FUNCIONES DE CHAT (MODO LIBRE) =====

/**
 * Selecciona un agente y abre el chat
 */
async function selectAgent(agentId) {
    try {
        // Enviar selección a la API
        const response = await fetch(`${API_BASE_URL}/api/agente/seleccionar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ agente_id: agentId })
        });

        if (!response.ok) throw new Error('Error al seleccionar agente');

        const data = await response.json();
        selectedAgent = agents.find(a => a.id === agentId);

        // Update UI
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.getElementById(`agent-${agentId}`).classList.add('selected');

        // Open chat
        openChat();

        // Add welcome message
        addMessage('agent', data.mensaje || `Hola, soy ${selectedAgent.nombre}. ¿En qué puedo ayudarte?`);

        showNotification(`Chat iniciado con ${selectedAgent.nombre}`, 'success');
    } catch (error) {
        console.error('Error al seleccionar agente:', error);
        showNotification('Error al conectar con el agente', 'error');
    }
}

/**
 * Abre el contenedor de chat
 */
function openChat() {
    const chatContainer = document.getElementById('chat-container');
    const chatTitle = document.getElementById('chat-title');

    if (selectedAgent) {
        chatTitle.textContent = `Chat con ${selectedAgent.nombre}`;
        chatTitle.style.color = selectedAgent.color;
    }

    chatContainer.style.display = 'block';

    // Clear previous messages
    document.getElementById('chat-messages').innerHTML = '';

    // Scroll to chat
    chatContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Cierra el contenedor de chat
 */
function closeChat() {
    document.getElementById('chat-container').style.display = 'none';
    selectedAgent = null;

    document.querySelectorAll('.agent-card').forEach(card => {
        card.classList.remove('selected');
    });
}

/**
 * Envía un mensaje al agente
 */
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) {
        showNotification('Por favor escribe un mensaje', 'warning');
        return;
    }

    if (!selectedAgent) {
        showNotification('Por favor selecciona un agente primero', 'warning');
        return;
    }

    // Add user message to chat
    addMessage('user', message);

    // Clear input
    input.value = '';

    // Disable send button
    const sendButton = document.getElementById('send-button');
    sendButton.disabled = true;
    sendButton.textContent = 'Enviando...';

    try {
        // Send to API
        const response = await fetch(`${API_BASE_URL}/api/mensaje`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: message,
                agente_id: selectedAgent.id
            })
        });

        if (!response.ok) throw new Error('Error al enviar mensaje');

        const data = await response.json();

        // Add agent response
        addMessage('agent', data.mensaje || 'Procesando tu solicitud...');

    } catch (error) {
        console.error('Error al enviar mensaje:', error);
        addMessage('agent', 'Lo siento, hubo un error al procesar tu mensaje. Por favor intenta de nuevo.');
    } finally {
        // Re-enable send button
        sendButton.disabled = false;
        sendButton.textContent = 'Enviar';
    }
}

/**
 * Añade un mensaje al chat
 */
function addMessage(sender, text) {
    const messagesContainer = document.getElementById('chat-messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message chat-message--${sender}`;

    const label = sender === 'user' ? 'Tú' : selectedAgent?.nombre || 'Agente';
    const labelDiv = document.createElement('div');
    labelDiv.className = 'chat-message__label';
    labelDiv.textContent = label;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'chat-message__bubble';
    bubbleDiv.textContent = text;

    if (sender === 'user') {
        messageDiv.appendChild(labelDiv);
        messageDiv.appendChild(bubbleDiv);
    } else {
        messageDiv.appendChild(labelDiv);
        messageDiv.appendChild(bubbleDiv);
    }

    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// ===== FUNCIONES DE EXPERIENCIAS GUIADAS =====

/**
 * Inicia una experiencia guiada
 */
function startExperience(experienceId) {
    currentExperience = experiences.find(exp => exp.id === experienceId);
    if (!currentExperience) return;

    currentStage = 0;

    // Show experience flow
    const flow = document.getElementById('experience-flow');
    const title = document.getElementById('experience-title');

    title.textContent = currentExperience.nombre;
    flow.style.display = 'block';

    // Render first stage
    renderStage();

    // Scroll to flow
    flow.scrollIntoView({ behavior: 'smooth' });

    showNotification(`Experiencia "${currentExperience.nombre}" iniciada`, 'success');
}

/**
 * Renderiza la etapa actual de la experiencia
 */
function renderStage() {
    if (!currentExperience) return;

    const stages = currentExperience.etapas;

    // Si no hay etapas (modo libre), mostrar mensaje especial
    if (stages.length === 0) {
        document.getElementById('experience-content').innerHTML = `
            <div class="text-center">
                <h3>Modo de Experimentación Libre</h3>
                <p>En este modo puedes interactuar con cualquiera de los agentes en el orden que prefieras.</p>
                <p>Vuelve al modo de exploración libre para comenzar.</p>
            </div>
        `;
        document.getElementById('prev-stage-btn').disabled = true;
        document.getElementById('next-stage-btn').disabled = true;
        return;
    }

    const stage = stages[currentStage];
    const agent = agents.find(a => a.id === stage.agente);

    // Update progress
    const progress = ((currentStage + 1) / stages.length) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = `Etapa ${currentStage + 1} de ${stages.length}`;

    // Update content
    document.getElementById('experience-content').innerHTML = `
        <div>
            <h3 style="color: ${agent?.color || '#2C5F2D'}">
                Etapa ${stage.orden}: ${stage.descripcion}
            </h3>
            <p style="margin-top: 1rem;">
                En esta etapa trabajarás con <strong>${agent?.nombre}</strong>: ${agent?.descripcion}
            </p>
            <div style="margin-top: 2rem;">
                <p><em>Aquí interactuarías con ${agent?.nombre}. Esta funcionalidad se completa con la integración real de los agentes.</em></p>
            </div>
        </div>
    `;

    // Update buttons
    document.getElementById('prev-stage-btn').disabled = currentStage === 0;
    document.getElementById('next-stage-btn').disabled = currentStage === stages.length - 1;

    if (currentStage === stages.length - 1) {
        document.getElementById('next-stage-btn').textContent = 'Finalizar';
    } else {
        document.getElementById('next-stage-btn').textContent = 'Siguiente →';
    }
}

/**
 * Avanza a la siguiente etapa
 */
function nextStage() {
    if (!currentExperience) return;

    if (currentStage < currentExperience.etapas.length - 1) {
        currentStage++;
        renderStage();
    } else {
        // Experiencia completada
        showNotification('¡Experiencia completada!', 'success');
        closeExperience();
    }
}

/**
 * Retrocede a la etapa anterior
 */
function prevStage() {
    if (!currentExperience) return;

    if (currentStage > 0) {
        currentStage--;
        renderStage();
    }
}

/**
 * Cierra la experiencia guiada
 */
function closeExperience() {
    document.getElementById('experience-flow').style.display = 'none';
    currentExperience = null;
    currentStage = 0;
}

// ===== EVENT LISTENERS =====

/**
 * Configura event listeners globales
 */
function setupEventListeners() {
    // Enter key in chat input
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
}

// ===== UTILIDADES =====

/**
 * Muestra una notificación temporal
 */
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;

    // Estilos inline (ya que no están en el CSS)
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '1rem 1.5rem';
    notification.style.borderRadius = '8px';
    notification.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '300px';
    notification.style.animation = 'slideIn 0.3s ease';

    // Colores según el tipo
    const colors = {
        'success': { bg: '#2C5F2D', text: '#fff' },
        'error': { bg: '#e74c3c', text: '#fff' },
        'warning': { bg: '#FFB03B', text: '#2C3E50' },
        'info': { bg: '#3498db', text: '#fff' }
    };

    const color = colors[type] || colors.info;
    notification.style.backgroundColor = color.bg;
    notification.style.color = color.text;

    // Añadir al body
    document.body.appendChild(notification);

    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Añadir animaciones CSS para notificaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('🌿 {DATAR} JavaScript cargado correctamente');
