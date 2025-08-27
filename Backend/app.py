from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple user credentials (in production, use proper authentication)
USERS = {
    "admin": "password123",
    "hr": "hrpass",
    "employee": "emp123"
}

# HR Bot knowledge base
HR_RESPONSES = {
    "leave": {
        "keywords": ["leave", "vacation", "time off", "holiday", "sick leave", "pto"],
        "response": "For leave requests: You can apply for leave through the HR portal. Annual leave: 21 days, Sick leave: 10 days. Submit requests at least 2 weeks in advance for planned leave."
    },
    "salary": {
        "keywords": ["salary", "pay", "payroll", "compensation", "wages", "bonus"],
        "response": "Salary queries: Your salary details are confidential. For salary reviews, speak with your manager. Payroll is processed on the last working day of each month. Bonuses are reviewed annually."
    },
    "benefits": {
        "keywords": ["benefits", "insurance", "health", "medical", "dental", "retirement", "401k"],
        "response": "Employee benefits include: Health insurance, Dental coverage, Vision care, 401(k) retirement plan with company matching, Life insurance. Contact HR for detailed benefit information."
    },
    "policy": {
        "keywords": ["policy", "handbook", "rules", "code of conduct", "dress code", "remote work"],
        "response": "Company policies: Please refer to the employee handbook. Dress code is business casual. Remote work policies vary by department. All policies are available on the company intranet."
    },
    "training": {
        "keywords": ["training", "development", "course", "learning", "certification", "skill"],
        "response": "Training & Development: We offer professional development courses, certification reimbursement, and internal training programs. Speak with your manager about training opportunities."
    },
    "contact": {
        "keywords": ["hr contact", "hr email", "hr phone", "hr department", "human resources"],
        "response": "HR Department Contact: Email: hr@company.com, Phone: (555) 123-4567, Office: Building A, Floor 2. Office hours: 9 AM - 5 PM, Monday to Friday."
    },
    "onboarding": {
        "keywords": ["new employee", "onboarding", "first day", "orientation", "welcome"],
        "response": "New Employee Onboarding: Welcome! Your first day includes orientation at 9 AM, IT setup, documentation completion, and team introductions. Bring ID and completed forms."
    },
    "performance": {
        "keywords": ["performance", "review", "evaluation", "appraisal", "feedback"],
        "response": "Performance Reviews: Annual reviews in December, mid-year check-ins in June. Self-evaluations due 1 week before review meetings. Goal setting and development planning included."
    }
}

def find_hr_response(message):
    """Find the most appropriate HR response based on keywords"""
    message_lower = message.lower()
    
    for category, data in HR_RESPONSES.items():
        for keyword in data["keywords"]:
            if keyword in message_lower:
                return data["response"]
    
    # Default response if no keywords match
    return "I'm here to help with HR-related questions! You can ask me about: leave policies, salary, benefits, company policies, training, HR contact info, onboarding, or performance reviews. How can I assist you today?"

@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        # Try to read from frontend folder first
        with open('../frontend/index.html', 'r') as file:
            html_content = file.read()
    except FileNotFoundError:
        try:
            # Fallback to same directory
            with open('index.html', 'r') as file:
                html_content = file.read()
        except FileNotFoundError:
            # If no HTML file found, return a basic template
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>HR Bot</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                    #login-screen, #chat-screen { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    input { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                    button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
                    button:hover { background: #0056b3; }
                    #messages { height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
                    .message { margin: 10px 0; padding: 10px; border-radius: 4px; }
                    .message.user { background: #e3f2fd; text-align: right; }
                    .message.bot { background: #f5f5f5; }
                    .message-header { font-size: 12px; margin-bottom: 5px; }
                    .timestamp { color: #666; }
                </style>
            </head>
            <body>
                <div id="login-screen">
                    <h2>HR Bot Login</h2>
                    <input type="text" id="username" placeholder="Username">
                    <input type="password" id="password" placeholder="Password">
                    <button id="confirm-btn">Login</button>
                </div>
                
                <div id="chat-screen" style="display:none;">
                    <h2>HR Assistant</h2>
                    <div id="messages"></div>
                    <div style="display:flex; gap:10px;">
                        <input type="text" id="message-input" placeholder="Type your HR question..." style="flex:1;">
                        <button id="send-btn">Send</button>
                    </div>
                </div>
                
                <script>
                    let currentUsername = '';
                    const loginScreen = document.getElementById('login-screen');
                    const chatScreen = document.getElementById('chat-screen');
                    const usernameInput = document.getElementById('username');
                    const passwordInput = document.getElementById('password');
                    const confirmBtn = document.getElementById('confirm-btn');
                    const messagesDiv = document.getElementById('messages');
                    const messageInput = document.getElementById('message-input');
                    const sendBtn = document.getElementById('send-btn');
                    
                    confirmBtn.addEventListener('click', handleLogin);
                    sendBtn.addEventListener('click', sendMessage);
                    messageInput.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') sendMessage();
                    });
                    
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
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ username, password })
                            });
                            
                            const data = await response.json();
                            
                            if (data.success) {
                                currentUsername = data.username;
                                loginScreen.style.display = 'none';
                                chatScreen.style.display = 'block';
                                addMessage('HR Bot', data.message, 'bot');
                                usernameInput.value = '';
                                passwordInput.value = '';
                            } else {
                                alert(data.message);
                            }
                        } catch (error) {
                            alert('Login failed. Please try again.');
                        }
                    }
                    
                    async function sendMessage() {
                        const message = messageInput.value.trim();
                        if (!message) return;
                        
                        addMessage(currentUsername, message, 'user');
                        messageInput.value = '';
                        
                        try {
                            const response = await fetch('/chat', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ message, username: currentUsername })
                            });
                            
                            const data = await response.json();
                            
                            if (data.success) {
                                addMessage('HR Bot', data.bot_response, 'bot');
                            } else {
                                addMessage('HR Bot', 'Sorry, I encountered an error.', 'bot');
                            }
                        } catch (error) {
                            addMessage('HR Bot', 'Connection error. Please try again.', 'bot');
                        }
                    }
                    
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
                </script>
            </body>
            </html>
            """
    return render_template_string(html_content)

@app.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if username in USERS and USERS[username] == password:
        return jsonify({
            "success": True,
            "message": f"Welcome {username}! I'm your HR assistant. How can I help you today?",
            "username": username
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password. Please try again."
        }), 401

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    username = data.get('username', 'User')
    
    if not user_message:
        return jsonify({
            "success": False,
            "message": "Please enter a message."
        }), 400
    
    # Get HR bot response
    bot_response = find_hr_response(user_message)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%H:%M")
    
    return jsonify({
        "success": True,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": timestamp,
        "username": username
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "HR Bot is running!", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("🤖 HR Bot Starting...")
    print("📋 Available login credentials:")
    for user, pwd in USERS.items():
        print(f"   Username: {user}, Password: {pwd}")
    print("\n🌐 Server will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)