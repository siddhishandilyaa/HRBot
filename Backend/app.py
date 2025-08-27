// Global variables
let currentUsername = '';

// DOM Elements
const loginScreen = document.getElementById('login-screen');
const chatScreen = document.getElementById('chat-screen');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const confirmBtn = document.getElementById('confirm-btn');
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

// Event listeners
confirmBtn.addEventListener('click', handleLogin);
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Handle login
async function handleLogin() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUsername = data.username;
            loginScreen.style.display = 'none';
            chatScreen.style.display = 'flex';
            
            // Show welcome message
            addMessage('HR Bot', data.message, 'bot');
            
            // Clear login fields
            usernameInput.value = '';
            passwordInput.value = '';
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please check your connection and try again.');
    }
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message to chat
    addMessage(currentUsername, message, 'user');
    messageInput.value = '';
    
    // Show typing indicator
    const typingIndicator = addMessage('HR Bot', 'Typing...', 'bot typing');
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                username: currentUsername
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        messagesDiv.removeChild(typingIndicator);
        
        if (data.success) {
            // Add bot response
            addMessage('HR Bot', data.bot_response, 'bot');
        } else {
            addMessage('HR Bot', 'Sorry, I encountered an error. Please try again.', 'bot error');
        }
    } catch (error) {
        console.error('Chat error:', error);
        // Remove typing indicator
        messagesDiv.removeChild(typingIndicator);
        addMessage('HR Bot', 'Connection error. Please check your internet and try again.', 'bot error');
    }
}

// Add message to chat
function addMessage(sender, message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <strong>${sender}</strong>
            <span class="timestamp">${time}</span>
        </div>
        <div class="message-content">${message}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    return messageDiv;
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('HR Bot loaded successfully!');
    usernameInput.focus();
});