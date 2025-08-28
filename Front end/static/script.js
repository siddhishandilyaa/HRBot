// Global variables
let currentUser = null;
let userRole = null;
let messageHistory = [];

// DOM elements
const loginOverlay = document.getElementById('loginOverlay');
const loginForm = document.getElementById('loginForm');
const loginError = document.getElementById('loginError');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

// Configuration
const API_BASE_URL = '';
const TYPING_DELAY = 1000;
const ERROR_DISPLAY_TIME = 5000;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    focusUsernameInput();
    checkStoredSession();
}

function setupEventListeners() {
    // Login form
    loginForm.addEventListener('submit', handleLogin);
    
    // Chat functionality
    sendButton.addEventListener('click', handleSendClick);
    messageInput.addEventListener('keypress', handleInputKeypress);
    messageInput.addEventListener('input', adjustTextareaHeight);
    
    // Feedback buttons
    setupFeedbackButtons();
    
    // Navigation tabs
    setupNavigationTabs();
}

function focusUsernameInput() {
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.focus();
    }
}

function checkStoredSession() {
    // Check if user was previously logged in (optional feature)
    const storedUser = sessionStorage.getItem('hrbot_user');
    const storedRole = sessionStorage.getItem('hrbot_role');
    
    if (storedUser && storedRole) {
        currentUser = storedUser;
        userRole = storedRole;
        hideLoginOverlay();
        enableChatInput();
        addWelcomeMessage();
    }
}

// Login functionality
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    
    if (!username || !password) {
        showLoginError('Please enter both username and password.');
        return;
    }
    
    try {
        showLoginLoading(true);
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            handleLoginSuccess(data);
        } else {
            showLoginError(data.message || 'Invalid credentials. Please try again.');
        }
    } catch (error) {
        console.error('Login error:', error);
        showLoginError('Connection error. Please check your internet connection and try again.');
    } finally {
        showLoginLoading(false);
    }
}

function handleLoginSuccess(data) {
    currentUser = data.username;
    userRole = data.role;
    
    // Store session (optional)
    sessionStorage.setItem('hrbot_user', currentUser);
    sessionStorage.setItem('hrbot_role', userRole);
    
    hideLoginOverlay();
    enableChatInput();
    
    // Add welcome message and action buttons
    addBotMessage(data.message);
    addActionButtons(data.role);
    
    // Update sidebar info
    updateSidebarInfo();
}

function showLoginError(message) {
    loginError.textContent = message;
    loginError.classList.remove('hidden');
    
    setTimeout(() => {
        loginError.classList.add('hidden');
    }, ERROR_DISPLAY_TIME);
}

function showLoginLoading(loading) {
    const loginBtn = document.querySelector('.login-btn');
    if (loading) {
        loginBtn.textContent = 'Logging in...';
        loginBtn.disabled = true;
    } else {
        loginBtn.textContent = 'Login';
        loginBtn.disabled = false;
    }
}

function hideLoginOverlay() {
    loginOverlay.classList.add('hidden');
}

function enableChatInput() {
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.placeholder = "Type a message...";
    messageInput.focus();
}

// Chat functionality
function handleSendClick() {
    const message = messageInput.value.trim();
    if (message) {
        sendMessage(message);
    }
}

function handleInputKeypress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
        }
    }
}

async function sendMessage(message) {
    if (!message.trim() || !currentUser) return;
    
    // Add message to history
    messageHistory.push({
        type: 'user',
        content: message,
        timestamp: new Date()
    });
    
    // Add user message to UI
    addUserMessage(message);
    
    // Clear input
    messageInput.value = '';
    adjustTextareaHeight();
    
    // Show typing indicator
    showTyping();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                username: currentUser
            })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTyping();
        
        if (data.success) {
            // Add bot response to history
            messageHistory.push({
                type: 'bot',
                content: data.bot_response,
                timestamp: new Date()
            });
            
            // Format and display bot response
            const formattedResponse = formatBotResponse(data.bot_response);
            addBotMessage(formattedResponse);
            
        } else {
            addBotMessage('Sorry, I encountered an error processing your request. Please try again.');
        }
    } catch (error) {
        console.error('Chat error:', error);
        hideTyping();
        addBotMessage('Connection error. Please check your internet connection and try again.');
    }
}

function formatBotResponse(response) {
    return response
        .replace(/<b>/g, '<strong>')
        .replace(/<\/b>/g, '</strong>')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function addBotMessage(content) {
    const time = getCurrentTime();
    const messageId = generateMessageId();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = messageId;
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar">HR</div>
            <div class="message-info">
                <span class="message-sender">HR Bot</span>
                <span class="message-time">${time}</span>
            </div>
        </div>
        <div class="message-content">${content}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    animateMessageIn(messageDiv);
}

function addUserMessage(content) {
    const time = getCurrentTime();
    const messageId = generateMessageId();
    const userInitial = currentUser ? currentUser.charAt(0).toUpperCase() : 'U';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.id = messageId;
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar">${userInitial}</div>
            <div class="message-info">
                <span class="message-sender">${currentUser || 'User'}</span>
                <span class="message-time">${time}</span>
            </div>
        </div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    animateMessageIn(messageDiv);
}

function addActionButtons(role) {
    const buttons = getActionButtons(role);
    if (buttons.length === 0) return;
    
    const actionDiv = document.createElement('div');
    actionDiv.className = 'action-buttons';
    
    buttons.forEach(button => {
        const btn = document.createElement('button');
        btn.className = 'action-btn';
        btn.textContent = button;
        btn.setAttribute('data-action', button.toLowerCase().replace(/\s+/g, '-'));
        btn.addEventListener('click', () => handleActionButton(button));
        actionDiv.appendChild(btn);
    });
    
    chatMessages.appendChild(actionDiv);
    scrollToBottom();
    animateMessageIn(actionDiv);
}

function getActionButtons(role) {
    const buttonConfig = {
        admin: [
            'Security Management',
            'AI Analytics', 
            'Disaster Recovery',
            'System Integration'
        ],
        hr: [
            'Individual Attendance',
            'Monthly Payroll',
            'Talent Pipeline', 
            'Wellness Dashboard'
        ],
        employee: [
            'Enhanced Profile',
            'Leave Balance',
            'Monthly Feedback',
            'Wellness Report'
        ],
        manager: [
            'Enhanced Profile',
            'Leave Balance',
            'Monthly Feedback',
            'Wellness Report'
        ]
    };
    
    return buttonConfig[role] || buttonConfig.employee;
}

function handleActionButton(buttonText) {
    // Send the action as a message
    sendMessage(buttonText);
}

// Typing indicator
function showTyping() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

function hideTyping() {
    typingIndicator.style.display = 'none';
}

// Feedback functionality
function setupFeedbackButtons() {
    document.querySelectorAll('.feedback-btn').forEach(btn => {
        btn.addEventListener('click', handleFeedbackClick);
    });
}

function handleFeedbackClick(e) {
    const btn = e.currentTarget;
    const feedback = btn.classList.contains('satisfied') ? 'satisfied' : 'not satisfied';
    
    // Visual feedback
    btn.style.transform = 'scale(0.95)';
    setTimeout(() => {
        btn.style.transform = '';
    }, 150);
    
    // Send feedback message
    addUserMessage(`I am ${feedback} with the service`);
    
    setTimeout(() => {
        addBotMessage('Thank you for your feedback! Your input helps us improve our service.');
    }, TYPING_DELAY);
}

// Navigation tabs
function setupNavigationTabs() {
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', handleTabClick);
    });
}

function handleTabClick(e) {
    e.preventDefault();
    const clickedTab = e.currentTarget;
    
    // Remove active class from all tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Add active class to clicked tab
    clickedTab.classList.add('active');
    
    // Handle tab-specific functionality
    const tabName = clickedTab.textContent.toLowerCase();
    handleTabChange(tabName);
}

function handleTabChange(tabName) {
    switch(tabName) {
        case 'chat':
            // Already on chat tab
            break;
        case 'files':
            addBotMessage('File sharing functionality will be available soon. You can currently share feedback and requests through chat.');
            break;
        case 'about':
            addBotMessage('HR Bot v3.1 - Your intelligent HR assistant. I can help with attendance, payroll, leave management, and employee services. Built with Flask and powered by advanced HR analytics.');
            break;
    }
}

// Utility functions
function getCurrentTime() {
    return new Date().toLocaleTimeString([], {
        hour: '2-digit', 
        minute: '2-digit'
    });
}

function generateMessageId() {
    return 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

function adjustTextareaHeight() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

function animateMessageIn(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 50);
}

function updateSidebarInfo() {
    const chatItemTime = document.querySelector('.chat-item-time');
    const chatItemPreview = document.querySelector('.chat-item-preview');
    
    if (chatItemTime) {
        chatItemTime.textContent = getCurrentTime();
    }
    
    if (chatItemPreview) {
        chatItemPreview.textContent = `Logged in as ${userRole}`;
    }
}

// Logout functionality
function logout() {
    currentUser = null;
    userRole = null;
    messageHistory = [];
    
    // Clear session storage
    sessionStorage.removeItem('hrbot_user');
    sessionStorage.removeItem('hrbot_role');
    
    // Reset UI
    loginOverlay.classList.remove('hidden');
    messageInput.disabled = true;
    sendButton.disabled = true;
    messageInput.placeholder = "Please login to chat...";
    
    // Clear login form
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    
    // Clear chat messages (optional)
    // chatMessages.innerHTML = '';
    
    // Focus username input
    focusUsernameInput();
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!messageInput.disabled && messageInput.value.trim()) {
            sendMessage(messageInput.value.trim());
        }
    }
    
    // Escape to clear input
    if (e.key === 'Escape' && document.activeElement === messageInput) {
        messageInput.value = '';
        adjustTextareaHeight();
    }
});

// Handle online/offline status
window.addEventListener('online', () => {
    addBotMessage('Connection restored. You can continue chatting.');
});

window.addEventListener('offline', () => {
    addBotMessage('Connection lost. Please check your internet connection.');
});

// Handle page visibility for better UX
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && currentUser) {
        // User returned to the tab, could refresh data or show updates
        console.log('User returned to HR Bot tab');
    }
});

// Add welcome message for first-time users
function addWelcomeMessage() {
    if (messageHistory.length === 0) {
        setTimeout(() => {
            addBotMessage('Welcome back! How can I assist you today?');
            if (userRole) {
                addActionButtons(userRole);
            }
        }, 500);
    }
}

// Error handling for unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    addBotMessage('An unexpected error occurred. Please refresh the page and try again.');
    event.preventDefault();
});

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        sendMessage,
        formatBotResponse,
        getCurrentTime,
        escapeHtml
    };
}
