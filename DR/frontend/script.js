// Medical RAG Chatbot - Frontend JavaScript

// Auto-detect if running on Vercel or localhost
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'  // Local development
    : '/api';  // Production (Vercel)

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

let conversationHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);
});

// Send message to API
async function sendMessage() {
    const query = userInput.value.trim();
    
    if (!query) return;

    // Disable input while processing
    userInput.disabled = true;
    sendButton.disabled = true;

    // Add user message to chat
    addMessage(query, 'user');
    
    // Clear input
    userInput.value = '';

    // Add loading indicator
    const loadingId = addLoadingMessage();

    try {
        // Call API
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                conversation_history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        // Remove loading indicator
        removeLoadingMessage(loadingId);

        // Add bot response
        addMessage(data.response, 'bot', data.sources);

        // Update conversation history
        conversationHistory.push(
            { role: 'user', content: query },
            { role: 'assistant', content: data.response }
        );

    } catch (error) {
        console.error('Error:', error);
        removeLoadingMessage(loadingId);
        addMessage('Sorry, I encountered an error. Please make sure the backend server is running on http://localhost:8000', 'bot');
    } finally {
        // Re-enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

// Add message to chat
function addMessage(content, sender, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const senderLabel = sender === 'user' ? 'You' : 'Medical Assistant';
    
    let html = `<strong>${senderLabel}:</strong><p>${content}</p>`;

    // Add sources if available
    if (sources && sources.length > 0) {
        html += '<div class="sources"><strong>Sources:</strong>';
        sources.forEach(source => {
            html += `<div>• ${source.title}</div>`;
        });
        html += '</div>';
    }

    contentDiv.innerHTML = html;
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add loading indicator
function addLoadingMessage() {
    const loadingId = 'loading-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = loadingId;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = `
        <strong>Medical Assistant:</strong>
        <p>
            <span class="loading"></span>
            <span class="loading"></span>
            <span class="loading"></span>
            Thinking...
        </p>
    `;

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return loadingId;
}

// Remove loading indicator
function removeLoadingMessage(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Check if backend is running
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('Backend is running');
            return true;
        }
    } catch (error) {
        console.warn('Backend is not running. Start it with: cd backend && python main.py');
        return false;
    }
}

// Check backend on load
checkBackendHealth();
