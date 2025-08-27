from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Enhanced user credentials with employee data
USERS = {
    "admin": {"password": "password123", "role": "admin", "emp_id": "EMP001"},
    "hr": {"password": "hrpass", "role": "hr", "emp_id": "EMP002"},
    "john.doe": {"password": "john123", "role": "employee", "emp_id": "EMP003"},
    "jane.smith": {"password": "jane123", "role": "employee", "emp_id": "EMP004"},
    "mike.johnson": {"password": "mike123", "role": "manager", "emp_id": "EMP005"},
    "sarah.wilson": {"password": "sarah123", "role": "employee", "emp_id": "EMP006"},
    "david.brown": {"password": "david123", "role": "employee", "emp_id": "EMP007"},
    "emily.davis": {"password": "emily123", "role": "employee", "emp_id": "EMP008"},
    "alex.miller": {"password": "alex123", "role": "employee", "emp_id": "EMP009"},
    "lisa.garcia": {"password": "lisa123", "role": "employee", "emp_id": "EMP010"},
    "tom.anderson": {"password": "tom123", "role": "employee", "emp_id": "EMP011"},
    "anna.taylor": {"password": "anna123", "role": "manager", "emp_id": "EMP012"},
    "chris.white": {"password": "chris123", "role": "employee", "emp_id": "EMP013"},
    "maya.lee": {"password": "maya123", "role": "employee", "emp_id": "EMP014"},
    "ryan.clark": {"password": "ryan123", "role": "employee", "emp_id": "EMP015"}
}

# Mock employee database
EMPLOYEE_DATA = {
    "EMP003": {
        "name": "John Doe", "department": "Engineering", "position": "Software Developer",
        "manager": "Mike Johnson", "hire_date": "2022-03-15", "salary": 75000,
        "leave_balance": {"annual": 18, "sick": 8}, "phone": "+1-555-0103"
    },
    "EMP004": {
        "name": "Jane Smith", "department": "Marketing", "position": "Marketing Specialist",
        "manager": "Anna Taylor", "hire_date": "2021-07-20", "salary": 65000,
        "leave_balance": {"annual": 15, "sick": 6}, "phone": "+1-555-0104"
    },
    "EMP005": {
        "name": "Mike Johnson", "department": "Engineering", "position": "Engineering Manager",
        "manager": "Admin", "hire_date": "2020-01-10", "salary": 95000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+1-555-0105"
    },
    "EMP006": {
        "name": "Sarah Wilson", "department": "Finance", "position": "Financial Analyst",
        "manager": "Anna Taylor", "hire_date": "2023-01-08", "salary": 70000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+1-555-0106"
    },
    "EMP007": {
        "name": "David Brown", "department": "Engineering", "position": "Senior Developer",
        "manager": "Mike Johnson", "hire_date": "2019-11-12", "salary": 85000,
        "leave_balance": {"annual": 12, "sick": 4}, "phone": "+1-555-0107"
    },
    "EMP008": {
        "name": "Emily Davis", "department": "HR", "position": "HR Coordinator",
        "manager": "HR", "hire_date": "2022-09-05", "salary": 55000,
        "leave_balance": {"annual": 16, "sick": 7}, "phone": "+1-555-0108"
    },
    "EMP009": {
        "name": "Alex Miller", "department": "Sales", "position": "Sales Representative",
        "manager": "Anna Taylor", "hire_date": "2023-06-01", "salary": 60000,
        "leave_balance": {"annual": 20, "sick": 9}, "phone": "+1-555-0109"
    },
    "EMP010": {
        "name": "Lisa Garcia", "department": "Design", "position": "UX Designer",
        "manager": "Mike Johnson", "hire_date": "2021-12-03", "salary": 72000,
        "leave_balance": {"annual": 14, "sick": 5}, "phone": "+1-555-0110"
    },
    "EMP011": {
        "name": "Tom Anderson", "department": "Operations", "position": "Operations Specialist",
        "manager": "Anna Taylor", "hire_date": "2020-08-17", "salary": 58000,
        "leave_balance": {"annual": 19, "sick": 8}, "phone": "+1-555-0111"
    },
    "EMP012": {
        "name": "Anna Taylor", "department": "Management", "position": "Department Manager",
        "manager": "Admin", "hire_date": "2018-04-22", "salary": 90000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+1-555-0112"
    },
    "EMP013": {
        "name": "Chris White", "department": "IT", "position": "System Administrator",
        "manager": "Mike Johnson", "hire_date": "2022-11-30", "salary": 68000,
        "leave_balance": {"annual": 17, "sick": 6}, "phone": "+1-555-0113"
    },
    "EMP014": {
        "name": "Maya Lee", "department": "Legal", "position": "Legal Assistant",
        "manager": "Anna Taylor", "hire_date": "2023-02-14", "salary": 52000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+1-555-0114"
    },
    "EMP015": {
        "name": "Ryan Clark", "department": "Engineering", "position": "Junior Developer",
        "manager": "Mike Johnson", "hire_date": "2023-09-12", "salary": 62000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+1-555-0115"
    }
}

def generate_attendance_data(emp_id, days=30):
    """Generate mock attendance data for the last N days"""
    attendance = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        # Skip weekends
        if date.weekday() >= 5:
            continue
            
        # 90% chance of being present
        status = "Present" if random.random() < 0.9 else random.choice(["Absent", "Half Day", "Work From Home"])
        
        if status == "Present":
            check_in = f"{random.randint(8, 10):02d}:{random.randint(0, 59):02d}"
            check_out = f"{random.randint(17, 19):02d}:{random.randint(0, 59):02d}"
        elif status == "Work From Home":
            check_in = f"{random.randint(9, 10):02d}:{random.randint(0, 59):02d}"
            check_out = f"{random.randint(17, 18):02d}:{random.randint(0, 59):02d}"
        else:
            check_in = check_out = "--"
        
        attendance.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%A"),
            "status": status,
            "check_in": check_in,
            "check_out": check_out
        })
    
    return sorted(attendance, key=lambda x: x['date'], reverse=True)

def get_employee_info(username):
    """Get employee information by username"""
    if username not in USERS:
        return None
    
    emp_id = USERS[username]["emp_id"]
    if emp_id not in EMPLOYEE_DATA:
        return None
    
    return EMPLOYEE_DATA[emp_id]

def find_hr_response(message, username):
    """Find the most appropriate HR response based on keywords"""
    message_lower = message.lower()
    emp_info = get_employee_info(username)
    
    # Attendance queries
    if any(word in message_lower for word in ["attendance", "present", "absent", "check in", "check out", "working hours"]):
        if emp_info:
            attendance = generate_attendance_data(USERS[username]["emp_id"], 10)
            present_days = len([a for a in attendance if a["status"] in ["Present", "Work From Home"]])
            response = f"📊 **Your Attendance Summary (Last 10 working days):**\n\n"
            response += f"Present: {present_days}/10 days\n\n"
            response += "**Recent Records:**\n"
            for record in attendance[:5]:
                response += f"• {record['date']} ({record['day']}): {record['status']}"
                if record['check_in'] != "--":
                    response += f" | In: {record['check_in']} Out: {record['check_out']}"
                response += "\n"
            return response
        return "I can show attendance records for logged-in employees only."
    
    # Profile/Personal information
    if any(word in message_lower for word in ["profile", "my info", "personal", "details", "about me"]):
        if emp_info:
            return f"👤 **Your Profile:**\n\n" \
                   f"**Name:** {emp_info['name']}\n" \
                   f"**Employee ID:** {USERS[username]['emp_id']}\n" \
                   f"**Department:** {emp_info['department']}\n" \
                   f"**Position:** {emp_info['position']}\n" \
                   f"**Manager:** {emp_info['manager']}\n" \
                   f"**Hire Date:** {emp_info['hire_date']}\n" \
                   f"**Contact:** {emp_info['phone']}"
        return "Profile information available for logged-in employees only."
    
    # Leave balance
    if any(word in message_lower for word in ["leave balance", "remaining leave", "vacation days", "sick days"]):
        if emp_info:
            return f"🏖️ **Your Leave Balance:**\n\n" \
                   f"**Annual Leave:** {emp_info['leave_balance']['annual']} days remaining\n" \
                   f"**Sick Leave:** {emp_info['leave_balance']['sick']} days remaining\n\n" \
                   f"💡 *Tip: Submit leave requests at least 2 weeks in advance for approval.*"
        return "Leave balance available for logged-in employees only."
    
    # Salary information
    if any(word in message_lower for word in ["salary", "pay", "payroll", "compensation", "wages"]):
        if emp_info and USERS[username]["role"] in ["admin", "hr"]:
            return f"💰 **Salary Information:**\n\n" \
                   f"**Annual Salary:** ${emp_info['salary']:,}\n" \
                   f"**Monthly Gross:** ${emp_info['salary']//12:,}\n\n" \
                   f"**Next Payroll:** {(datetime.now().replace(day=28) + timedelta(days=4)).strftime('%B %d, %Y')}\n" \
                   f"💡 *For detailed pay stubs, check your email or HR portal.*"
        elif emp_info:
            return "💰 **Salary Information:**\n\nFor salary details and pay stubs, please contact HR directly or check your employee portal. Salary information is confidential and available through secure channels only."
        return "Salary information available for logged-in employees only."
    
    # Manager information
    if any(word in message_lower for word in ["manager", "supervisor", "boss", "reporting"]):
        if emp_info:
            return f"👥 **Reporting Structure:**\n\n" \
                   f"**Your Manager:** {emp_info['manager']}\n" \
                   f"**Department:** {emp_info['department']}\n\n" \
                   f"💡 *For scheduling meetings or feedback, please reach out directly to your manager.*"
        return "Manager information available for logged-in employees only."
    
    # Department colleagues
    if any(word in message_lower for word in ["colleagues", "team", "department", "coworkers"]):
        if emp_info:
            dept = emp_info['department']
            colleagues = [data['name'] for emp_id, data in EMPLOYEE_DATA.items() 
                         if data['department'] == dept and data['name'] != emp_info['name']]
            
            if colleagues:
                return f"👥 **Your {dept} Department Colleagues:**\n\n" + \
                       "\n".join([f"• {colleague}" for colleague in colleagues[:8]]) + \
                       f"\n\n💡 *Contact HR for detailed contact information.*"
            return f"You're currently the only member listed in the {dept} department."
        return "Department information available for logged-in employees only."
    
    # Original categories with enhanced responses
    if any(word in message_lower for word in ["leave", "vacation", "time off", "holiday", "sick leave", "pto"]):
        return "🏖️ **Leave Policy:**\n\n" \
               "• **Annual Leave:** 21 days per year\n" \
               "• **Sick Leave:** 10 days per year\n" \
               "• **Personal Days:** 3 days per year\n" \
               "• **Maternity/Paternity:** 12 weeks\n\n" \
               "📝 **How to Apply:**\n" \
               "1. Submit request through HR portal\n" \
               "2. Get manager approval\n" \
               "3. Submit at least 2 weeks in advance\n\n" \
               "💡 *Emergency leaves can be applied retroactively with proper documentation.*"
    
    if any(word in message_lower for word in ["benefits", "insurance", "health", "medical", "dental", "retirement", "401k"]):
        return "🏥 **Employee Benefits Package:**\n\n" \
               "**Health & Wellness:**\n" \
               "• Medical Insurance (90% company paid)\n" \
               "• Dental & Vision Coverage\n" \
               "• Mental Health Support\n" \
               "• Gym Membership Reimbursement\n\n" \
               "**Financial:**\n" \
               "• 401(k) with 6% company match\n" \
               "• Life Insurance (2x annual salary)\n" \
               "• Disability Insurance\n\n" \
               "📞 Contact HR at hr@company.com for enrollment details."
    
    if any(word in message_lower for word in ["policy", "handbook", "rules", "code of conduct", "dress code", "remote work"]):
        return "📋 **Company Policies:**\n\n" \
               "• **Employee Handbook:** Available on company intranet\n" \
               "• **Dress Code:** Business casual (Mon-Thu), Casual Friday\n" \
               "• **Remote Work:** Hybrid policy - 3 days office, 2 days remote\n" \
               "• **Working Hours:** 9 AM - 6 PM (flexible start between 8-10 AM)\n" \
               "• **Code of Conduct:** Zero tolerance for harassment\n\n" \
               "📖 *Full policies available at: company-intranet.com/policies*"
    
    if any(word in message_lower for word in ["training", "development", "course", "learning", "certification", "skill"]):
        return "📚 **Learning & Development:**\n\n" \
               "**Available Programs:**\n" \
               "• Technical skill courses (Coursera, Udemy)\n" \
               "• Leadership development workshops\n" \
               "• Industry certifications (up to $2000/year reimbursement)\n" \
               "• Internal mentorship program\n" \
               "• Conference attendance budget\n\n" \
               "💡 *Discuss your development goals with your manager during your next 1:1.*"
    
    if any(word in message_lower for word in ["hr contact", "hr email", "hr phone", "hr department", "human resources"]):
        return "📞 **HR Department Contact:**\n\n" \
               "• **Email:** hr@company.com\n" \
               "• **Phone:** (555) 123-4567\n" \
               "• **Location:** Building A, Floor 2, Room 201\n" \
               "• **Hours:** 9 AM - 5 PM, Monday to Friday\n\n" \
               "**HR Team:**\n" \
               "• Sarah Johnson - HR Director\n" \
               "• Emily Davis - HR Coordinator\n" \
               "• Mike Roberts - Benefits Specialist"
    
    # Default response with personalization
    name = emp_info['name'] if emp_info else username
    return f"👋 Hi {name}! I'm here to help with HR questions.\n\n" \
           "**I can help you with:**\n" \
           "• 📊 Attendance records\n• 👤 Your profile information\n• 🏖️ Leave balance & policies\n" \
           "• 💰 Salary information\n• 👥 Manager & team details\n• 🏥 Benefits information\n" \
           "• 📋 Company policies\n• 📚 Training opportunities\n• 📞 HR contact information\n\n" \
           "What would you like to know about?"

@app.route('/')
def index():
    """Serve the main HTML page with enhanced UI"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TechCorp HR Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container { 
                background: rgba(255, 255, 255, 0.95); 
                border-radius: 20px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 800px;
                width: 100%;
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { opacity: 0.9; font-size: 1.1em; }
            .content { padding: 40px; }
            
            #login-screen input { 
                width: 100%; 
                padding: 15px 20px; 
                margin: 10px 0; 
                border: 2px solid #e0e0e0; 
                border-radius: 10px; 
                font-size: 16px;
                transition: border-color 0.3s;
            }
            #login-screen input:focus {
                border-color: #4facfe;
                outline: none;
            }
            button { 
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: 600;
                transition: transform 0.3s;
                width: 100%;
                margin-top: 10px;
            }
            button:hover { transform: translateY(-2px); }
            
            .demo-users {
                background: #f8f9ff;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }
            .demo-users h3 { color: #333; margin-bottom: 15px; }
            .user-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
            }
            .user-item {
                background: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid #e0e0e0;
            }
            
            #messages { 
                height: 500px; 
                overflow-y: auto; 
                border: 2px solid #e0e0e0; 
                border-radius: 15px;
                padding: 20px; 
                margin-bottom: 20px; 
                background: #fafafa;
            }
            .message { 
                margin: 15px 0; 
                padding: 15px 20px; 
                border-radius: 15px; 
                max-width: 80%;
                word-wrap: break-word;
            }
            .message.user { 
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                margin-left: auto;
                text-align: right; 
            }
            .message.bot { 
                background: white;
                border: 2px solid #e0e0e0;
                color: #333;
            }
            .message-header { font-size: 12px; margin-bottom: 8px; font-weight: 600; }
            .timestamp { opacity: 0.7; }
            .message-content { line-height: 1.6; white-space: pre-line; }
            
            .input-area {
                display: flex;
                gap: 15px;
                align-items: flex-end;
            }
            #message-input {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                font-size: 16px;
                resize: vertical;
                min-height: 50px;
                max-height: 120px;
            }
            #message-input:focus {
                border-color: #4facfe;
                outline: none;
            }
            #send-btn {
                width: auto;
                margin: 0;
                padding: 15px 25px;
                border-radius: 15px;
            }
            
            .status-bar {
                background: #f0f0f0;
                padding: 10px 20px;
                font-size: 14px;
                color: #666;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .user-info { font-weight: 600; color: #4facfe; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 TechCorp HR Assistant</h1>
                <p>Your personal HR support, available 24/7</p>
            </div>
            
            <div class="content">
                <div id="login-screen">
                    <h2 style="margin-bottom: 20px; color: #333;">Welcome Back!</h2>
                    <input type="text" id="username" placeholder="Enter your username">
                    <input type="password" id="password" placeholder="Enter your password">
                    <button id="confirm-btn">Sign In</button>
                    
                    <div class="demo-users">
                        <h3>👥 Demo User Accounts</h3>
                        <div class="user-grid">
                            <div class="user-item"><strong>john.doe</strong> / john123</div>
                            <div class="user-item"><strong>jane.smith</strong> / jane123</div>
                            <div class="user-item"><strong>mike.johnson</strong> / mike123</div>
                            <div class="user-item"><strong>sarah.wilson</strong> / sarah123</div>
                            <div class="user-item"><strong>admin</strong> / password123</div>
                            <div class="user-item"><strong>hr</strong> / hrpass</div>
                        </div>
                    </div>
                </div>
                
                <div id="chat-screen" style="display:none;">
                    <div class="status-bar">
                        <span>🟢 Connected to HR Assistant</span>
                        <span class="user-info" id="current-user"></span>
                    </div>
                    <div id="messages"></div>
                    <div class="input-area">
                        <textarea id="message-input" placeholder="Ask me about attendance, leave balance, benefits, policies, or anything HR related..."></textarea>
                        <button id="send-btn">Send 📤</button>
                    </div>
                </div>
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
            const currentUserSpan = document.getElementById('current-user');
            
            confirmBtn.addEventListener('click', handleLogin);
            sendBtn.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            // Demo user click handlers
            document.querySelectorAll('.user-item').forEach(item => {
                item.addEventListener('click', function() {
                    const text = this.textContent;
                    const [username, password] = text.split(' / ');
                    usernameInput.value = username;
                    passwordInput.value = password;
                });
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
                        currentUserSpan.textContent = `Logged in as: ${currentUsername}`;
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
    """Handle user login with enhanced validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid request format."}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required."}), 400
        
        if username in USERS and USERS[username]["password"] == password:
            emp_info = get_employee_info(username)
            welcome_msg = f"Welcome back, {emp_info['name'] if emp_info else username}! 👋\n\n"
            welcome_msg += "I'm your HR assistant. I can help you with:\n"
            welcome_msg += "• 📊 Check your attendance records\n"
            welcome_msg += "• 🏖️ View leave balance\n"
            welcome_msg += "• 👤 Access your profile information\n"
            welcome_msg += "• 💰 Salary and benefits information\n"
            welcome_msg += "• 📋 Company policies and procedures\n\n"
            welcome_msg += "What would you like to know about today?"
            
            return jsonify({
                "success": True,
                "message": welcome_msg,
                "username": username,
                "role": USERS[username]["role"]
            })
        else:
            return jsonify({
                "success": False,
                "message": "Invalid credentials. Please check your username and password."
            }), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug logging
        return jsonify({
            "success": False,
            "message": "Server error during login. Please try again."
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with enhanced error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request format."
            }), 400
            
        user_message = data.get('message', '').strip()
        username = data.get('username', 'User')
        
        if not user_message:
            return jsonify({
                "success": False,
                "message": "Please enter a message."
            }), 400
        
        if not username or username not in USERS:
            return jsonify({
                "success": False,
                "message": "Please log in first."
            }), 401
        
        # Get HR bot response with user context
        bot_response = find_hr_response(user_message, username)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        return jsonify({
            "success": True,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": timestamp,
            "username": username
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Debug logging
        return jsonify({
            "success": False,
            "message": "Sorry, I encountered an error processing your request."
        }), 500

@app.route('/employee/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    """API endpoint to get employee data (for admin/hr users)"""
    try:
        # In a real app, you'd verify the requesting user has appropriate permissions
        if emp_id in EMPLOYEE_DATA:
            return jsonify({
                "success": True,
                "employee": EMPLOYEE_DATA[emp_id]
            })
        else:
            return jsonify({
                "success": False,
                "message": "Employee not found."
            }), 404
            
    except Exception as e:
        print(f"Employee lookup error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Server error during employee lookup."
        }), 500

@app.route('/attendance/<username>', methods=['GET'])
def get_attendance(username):
    """API endpoint to get attendance data"""
    try:
        if username not in USERS:
            return jsonify({
                "success": False,
                "message": "User not found."
            }), 404
            
        emp_id = USERS[username]["emp_id"]
        days = request.args.get('days', 30, type=int)
        attendance_data = generate_attendance_data(emp_id, days)
        
        return jsonify({
            "success": True,
            "attendance": attendance_data,
            "employee_id": emp_id,
            "days_requested": days
        })
        
    except Exception as e:
        print(f"Attendance lookup error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Server error during attendance lookup."
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Enhanced health check endpoint"""
    return jsonify({
        "status": "HR Bot is running smoothly! 🤖",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0",
        "employees_loaded": len(EMPLOYEE_DATA),
        "users_configured": len(USERS)
    })

@app.route('/debug/users', methods=['GET'])
def debug_users():
    """Debug endpoint to list available users (remove in production!)"""
    user_list = []
    for username, data in USERS.items():
        emp_info = get_employee_info(username)
        user_list.append({
            "username": username,
            "role": data["role"],
            "name": emp_info["name"] if emp_info else "N/A",
            "department": emp_info["department"] if emp_info else "N/A"
        })
    
    return jsonify({
        "total_users": len(USERS),
        "users": user_list
    })

if __name__ == '__main__':
    print("🤖 Enhanced HR Bot Starting...")
    print("=" * 50)
    print("📋 Sample login credentials:")
    print("-" * 30)
    
    sample_users = ["john.doe", "jane.smith", "mike.johnson", "admin", "hr"]
    for user in sample_users:
        if user in USERS:
            emp_info = get_employee_info(user)
            name = emp_info["name"] if emp_info else "N/A"
            role = USERS[user]["role"]
            print(f"   👤 {user:<12} | {USERS[user]['password']:<10} | {role:<8} | {name}")
    
    print("-" * 30)
    print(f"👥 Total employees loaded: {len(EMPLOYEE_DATA)}")
    print(f"🔐 Total user accounts: {len(USERS)}")
    print("\n🌐 Server starting at: http://localhost:5000")
    print("🛠️  Debug endpoints:")
    print("   • /health - System status")
    print("   • /debug/users - User list")
    print("   • /attendance/<username> - Attendance API")
    print("   • /employee/<emp_id> - Employee API")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {str(e)}")
        print("🔍 Check the error details above for debugging")