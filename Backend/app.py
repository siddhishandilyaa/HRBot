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
    with open('index.html', 'r') as file:
        html_content = file.read()
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