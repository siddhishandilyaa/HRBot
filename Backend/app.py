from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime, date
import uuid
import json
from flask import render_template

app = Flask(__name__,template_folder="../Front end",static_folder="../Front end/static")
app.secret_key = 'your-secret-key-change-in-production'
CORS(app)

# In-memory storage (replace with database in production)
conversations = {}
tickets = []
employees = {}
leave_requests = []
dependents = []
holidays = [
    {'date': '2025-01-01', 'holiday': 'New Year\'s Day'},
    {'date': '2025-01-26', 'holiday': 'Republic Day'},
    {'date': '2025-03-14', 'holiday': 'Holi'},
    {'date': '2025-08-15', 'holiday': 'Independence Day'},
    {'date': '2025-10-02', 'holiday': 'Gandhi Jayanti'},
    {'date': '2025-12-25', 'holiday': 'Christmas Day'}
]
benefit_plans = [
    {'plan': 'Health Insurance', 'coverage': 'Medical, Dental, Vision', 'premium': '$150/month'},
    {'plan': 'Retirement Plan', 'coverage': '401(k) with 5% match', 'premium': 'Company matched'},
    {'plan': 'Life Insurance', 'coverage': '2x annual salary', 'premium': '$25/month'},
    {'plan': 'Disability Insurance', 'coverage': 'Short & Long term', 'premium': '$40/month'}
]

# HR Bot responses and actions
HR_RESPONSES = {
    'greeting': "Hi Siddhi, how may I help you today?",
    'thanks': "Thank you for your valuable feedback\n\nSee you! Bye :)",
    'help': "Please choose an issue you need assistance with or just type your issue."
}

HR_ACTIONS = [
    {'id': 'apply_leave', 'label': 'Apply leave'},
    {'id': 'get_benefit_plans', 'label': 'Get benefit plans'},
    {'id': 'get_salary_details', 'label': 'Get salary details'},
    {'id': 'holiday_list', 'label': 'Holiday list'},
    {'id': 'create_ticket', 'label': 'Create ticket'},
    {'id': 'get_ticket_details', 'label': 'Get ticket details'},
    {'id': 'add_employee_dependent', 'label': 'Add employee dependent'}
]

def generate_id():
    """Generate a unique ID"""
    return str(uuid.uuid4())

def generate_short_id():
    """Generate a short ID for tickets"""
    return str(uuid.uuid4())[:8]
@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html') 

@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    """Initialize a new chat session"""
    session_id = generate_id()
    conversations[session_id] = {
        'messages': [
            {
                'id': generate_id(),
                'sender': 'bot',
                'message': HR_RESPONSES['greeting'],
                'timestamp': datetime.now().isoformat(),
                'actions': HR_ACTIONS
            }
        ],
        'created_at': datetime.now().isoformat(),
        'last_read': datetime.now().isoformat()
    }
    
    return jsonify({
        'session_id': session_id,
        'message': 'Chat session started',
        'initial_response': conversations[session_id]['messages'][0]
    })

@app.route('/api/chat/<session_id>/send', methods=['POST'])
def send_message(session_id):
    """Send a message in the chat"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    action = data.get('action', None)
    
    if session_id not in conversations:
        return jsonify({'error': 'Invalid session'}), 404
    
    # Add user message if there's text content
    response_data = {}
    if user_message:
        user_msg = {
            'id': generate_id(),
            'sender': 'user',
            'message': user_message,
            'timestamp': datetime.now().isoformat()
        }
        conversations[session_id]['messages'].append(user_msg)
        response_data['user_message'] = user_msg
    
    # Generate bot response based on action or message
    bot_response = generate_bot_response(user_message, action, session_id)
    conversations[session_id]['messages'].append(bot_response)
    response_data['bot_response'] = bot_response
    
    # Update last_read timestamp
    conversations[session_id]['last_read'] = datetime.now().isoformat()
    
    return jsonify(response_data)

def generate_bot_response(message, action, session_id):
    """Generate appropriate bot response"""
    bot_msg = {
        'id': generate_id(),
        'sender': 'bot',
        'timestamp': datetime.now().isoformat()
    }
    
    if action:
        if action == 'apply_leave':
            bot_msg['message'] = "I'll help you apply for leave. Please provide the following details:"
            bot_msg['form'] = {
                'type': 'leave_application',
                'fields': [
                    {'name': 'leave_type', 'label': 'Leave Type', 'type': 'select', 'required': True,
                     'options': ['Annual Leave', 'Sick Leave', 'Personal Leave', 'Emergency Leave', 'Maternity Leave']},
                    {'name': 'start_date', 'label': 'Start Date', 'type': 'date', 'required': True},
                    {'name': 'end_date', 'label': 'End Date', 'type': 'date', 'required': True},
                    {'name': 'reason', 'label': 'Reason for Leave', 'type': 'textarea', 'required': True, 'placeholder': 'Please provide a brief reason for your leave request'}
                ]
            }
        
        elif action == 'get_benefit_plans':
            bot_msg['message'] = "Here are the available benefit plans for employees:"
            bot_msg['data'] = {
                'type': 'benefit_plans',
                'plans': benefit_plans
            }
            bot_msg['actions'] = [
                {'id': 'enroll_benefit', 'label': 'Enroll in Benefits'},
                {'id': 'benefit_details', 'label': 'Get More Details'}
            ]
        
        elif action == 'get_salary_details':
            bot_msg['message'] = "Here are your current salary details:"
            bot_msg['data'] = {
                'type': 'salary_details',
                'details': {
                    'employee_id': 'EMP001',
                    'basic_salary': '$5,000',
                    'house_allowance': '$800',
                    'transport_allowance': '$200',
                    'medical_allowance': '$150',
                    'gross_salary': '$6,150',
                    'tax_deduction': '$500',
                    'pf_deduction': '$300',
                    'insurance_premium': '$150',
                    'net_salary': '$5,200',
                    'pay_date': '28th of every month',
                    'last_updated': '2025-08-01'
                }
            }
        
        elif action == 'holiday_list':
            bot_msg['message'] = "Here's the official holiday list for 2025:"
            bot_msg['data'] = {
                'type': 'holidays',
                'year': 2025,
                'holidays': holidays
            }
        
        elif action == 'create_ticket':
            bot_msg['message'] = "I'll help you create a support ticket. Please provide the following information:"
            bot_msg['form'] = {
                'type': 'ticket_creation',
                'fields': [
                    {'name': 'category', 'label': 'Category', 'type': 'select', 'required': True,
                     'options': ['IT Support', 'HR Query', 'Payroll Issue', 'Benefits', 'Equipment Request', 'Other']},
                    {'name': 'priority', 'label': 'Priority Level', 'type': 'select', 'required': True,
                     'options': ['Low', 'Medium', 'High', 'Critical']},
                    {'name': 'subject', 'label': 'Subject', 'type': 'text', 'required': True, 'placeholder': 'Brief description of the issue'},
                    {'name': 'description', 'label': 'Detailed Description', 'type': 'textarea', 'required': True,
                     'placeholder': 'Please provide detailed information about your request or issue'}
                ]
            }
        
        elif action == 'get_ticket_details':
            bot_msg['message'] = "I can help you check your ticket status. Here are your recent tickets:"
            user_tickets = [t for t in tickets if t.get('created_by') == session_id]
            if user_tickets:
                bot_msg['data'] = {
                    'type': 'user_tickets',
                    'tickets': user_tickets[-5:]  # Show last 5 tickets
                }
            else:
                bot_msg['message'] = "You don't have any support tickets yet. Would you like to create one?"
                bot_msg['actions'] = [{'id': 'create_ticket', 'label': 'Create New Ticket'}]
        
        elif action == 'add_employee_dependent':
            bot_msg['message'] = "I'll help you add a family dependent to your profile. Please provide the required information:"
            bot_msg['form'] = {
                'type': 'add_dependent',
                'fields': [
                    {'name': 'dependent_name', 'label': 'Full Name', 'type': 'text', 'required': True},
                    {'name': 'relationship', 'label': 'Relationship', 'type': 'select', 'required': True,
                     'options': ['Spouse', 'Son', 'Daughter', 'Father', 'Mother', 'Brother', 'Sister']},
                    {'name': 'date_of_birth', 'label': 'Date of Birth', 'type': 'date', 'required': True},
                    {'name': 'gender', 'label': 'Gender', 'type': 'select', 'required': True,
                     'options': ['Male', 'Female', 'Other']},
                    {'name': 'phone', 'label': 'Phone Number', 'type': 'text', 'required': False},
                    {'name': 'emergency_contact', 'label': 'Emergency Contact', 'type': 'checkbox', 'required': False}
                ]
            }
        
        # Additional actions
        elif action == 'enroll_benefit':
            bot_msg['message'] = "To enroll in benefits, please contact HR at hr@company.com or call ext. 1234. Open enrollment period is from November 1-30 each year."
        
        elif action == 'benefit_details':
            bot_msg['message'] = "For detailed benefit information including coverage limits, deductibles, and provider networks, please visit our employee portal or contact HR."
    
    else:
        # Handle text-based queries
        message_lower = message.lower() if message else ''
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            bot_msg['message'] = HR_RESPONSES['greeting']
            bot_msg['actions'] = HR_ACTIONS
        
        # Farewell responses
        elif any(word in message_lower for word in ['bye', 'goodbye', 'thank you', 'thanks']):
            bot_msg['message'] = HR_RESPONSES['thanks']
        
        # Help or unclear messages
        elif any(word in message_lower for word in ['help', 'assist', 'support']) or message_lower == '':
            bot_msg['message'] = HR_RESPONSES['help']
            bot_msg['actions'] = HR_ACTIONS
        
        # Specific keyword responses
        elif any(word in message_lower for word in ['leave', 'vacation', 'time off']):
            bot_msg['message'] = "I can help you with leave applications. Would you like to apply for leave?"
            bot_msg['actions'] = [{'id': 'apply_leave', 'label': 'Apply for Leave'}]
        
        elif any(word in message_lower for word in ['salary', 'pay', 'payroll']):
            bot_msg['message'] = "I can show you your salary details. Would you like to view them?"
            bot_msg['actions'] = [{'id': 'get_salary_details', 'label': 'View Salary Details'}]
        
        elif any(word in message_lower for word in ['holiday', 'holidays']):
            bot_msg['message'] = "Would you like to see the holiday calendar?"
            bot_msg['actions'] = [{'id': 'holiday_list', 'label': 'View Holiday List'}]
        
        elif any(word in message_lower for word in ['ticket', 'issue', 'problem']):
            bot_msg['message'] = "I can help you create a support ticket or check existing ones."
            bot_msg['actions'] = [
                {'id': 'create_ticket', 'label': 'Create New Ticket'},
                {'id': 'get_ticket_details', 'label': 'Check My Tickets'}
            ]
        
        elif any(word in message_lower for word in ['benefit', 'insurance', 'medical']):
            bot_msg['message'] = "Would you like to see available benefit plans?"
            bot_msg['actions'] = [{'id': 'get_benefit_plans', 'label': 'View Benefit Plans'}]
        
        # Default response
        else:
            bot_msg['message'] = "I understand you need assistance. " + HR_RESPONSES['help']
            bot_msg['actions'] = HR_ACTIONS
    
    return bot_msg

@app.route('/api/chat/<session_id>/submit-form', methods=['POST'])
def submit_form(session_id):
    """Handle form submissions"""
    data = request.get_json()
    form_type = data.get('form_type')
    form_data = data.get('form_data')
    
    if session_id not in conversations:
        return jsonify({'error': 'Invalid session'}), 404
    
    response_msg = {
        'id': generate_id(),
        'sender': 'bot',
        'timestamp': datetime.now().isoformat(),
        'feedback_request': True
    }
    
    if form_type == 'leave_application':
        # Process leave application
        leave_id = generate_short_id()
        leave_request = {
            'id': leave_id,
            'employee_id': session_id,
            'leave_type': form_data.get('leave_type'),
            'start_date': form_data.get('start_date'),
            'end_date': form_data.get('end_date'),
            'reason': form_data.get('reason'),
            'status': 'Pending',
            'applied_on': datetime.now().isoformat(),
            'days_requested': calculate_leave_days(form_data.get('start_date'), form_data.get('end_date'))
        }
        leave_requests.append(leave_request)
        
        response_msg['message'] = f"✅ Your leave application has been submitted successfully!\n\n📋 Request ID: {leave_id}\n📅 Leave Type: {form_data.get('leave_type')}\n🗓️ Duration: {form_data.get('start_date')} to {form_data.get('end_date')}\n\nYour manager will review and respond within 2 business days. You'll receive an email notification once approved."
        
    elif form_type == 'ticket_creation':
        # Process ticket creation
        ticket_id = generate_short_id()
        ticket = {
            'id': ticket_id,
            'category': form_data.get('category'),
            'priority': form_data.get('priority'),
            'subject': form_data.get('subject'),
            'description': form_data.get('description'),
            'status': 'Open',
            'created_by': session_id,
            'created_on': datetime.now().isoformat(),
            'assigned_to': None,
            'estimated_resolution': get_estimated_resolution(form_data.get('priority'))
        }
        tickets.append(ticket)
        
        response_msg['message'] = f"🎫 Your support ticket has been created successfully!\n\n🆔 Ticket ID: {ticket_id}\n📊 Priority: {form_data.get('priority')}\n📂 Category: {form_data.get('category')}\n⏱️ Expected Resolution: {ticket['estimated_resolution']}\n\nOur support team will respond within the expected timeframe. You can check your ticket status anytime."
        
    elif form_type == 'add_dependent':
        # Process dependent addition
        dependent_id = generate_id()
        dependent = {
            'id': dependent_id,
            'employee_id': session_id,
            'name': form_data.get('dependent_name'),
            'relationship': form_data.get('relationship'),
            'date_of_birth': form_data.get('date_of_birth'),
            'gender': form_data.get('gender'),
            'phone': form_data.get('phone', ''),
            'emergency_contact': form_data.get('emergency_contact', False),
            'added_on': datetime.now().isoformat(),
            'age': calculate_age(form_data.get('date_of_birth'))
        }
        dependents.append(dependent)
        
        if session_id not in employees:
            employees[session_id] = {'dependents': []}
        employees[session_id]['dependents'].append(dependent)
        
        response_msg['message'] = f"👨‍👩‍👧‍👦 Dependent '{dependent['name']}' has been added successfully to your profile!\n\n👤 Name: {dependent['name']}\n🤝 Relationship: {dependent['relationship']}\n🎂 Age: {dependent['age']} years\n\nThey are now eligible for company benefits. HR will process the enrollment within 3-5 business days."
    
    conversations[session_id]['messages'].append(response_msg)
    
    return jsonify({'bot_response': response_msg})

def calculate_leave_days(start_date, end_date):
    """Calculate number of leave days"""
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return (end - start).days + 1
    except:
        return 0

def calculate_age(birth_date):
    """Calculate age from birth date"""
    try:
        from datetime import datetime
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except:
        return 0

def get_estimated_resolution(priority):
    """Get estimated resolution time based on priority"""
    resolution_times = {
        'Critical': '4 hours',
        'High': '24 hours',
        'Medium': '3 business days',
        'Low': '5 business days'
    }
    return resolution_times.get(priority, '5 business days')

@app.route('/api/chat/<session_id>/feedback', methods=['POST'])
def submit_feedback(session_id):
    """Handle feedback submission"""
    data = request.get_json()
    feedback_type = data.get('type')  # 'satisfied' or 'not_satisfied'
    
    # Store feedback
    feedback_entry = {
        'id': generate_id(),
        'session_id': session_id,
        'type': feedback_type,
        'timestamp': datetime.now().isoformat()
    }
    
    feedback_msg = {
        'id': generate_id(),
        'sender': 'bot',
        'message': HR_RESPONSES['thanks'],
        'timestamp': datetime.now().isoformat()
    }
    
    if session_id in conversations:
        conversations[session_id]['messages'].append(feedback_msg)
        conversations[session_id]['feedback'] = feedback_entry
    
    return jsonify({
        'message': 'Feedback received successfully',
        'bot_response': feedback_msg
    })

@app.route('/api/chat/<session_id>/history', methods=['GET'])
def get_chat_history(session_id):
    """Get chat history for a session"""
    if session_id not in conversations:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'session_id': session_id,
        'messages': conversations[session_id]['messages'],
        'created_at': conversations[session_id]['created_at'],
        'last_read': conversations[session_id].get('last_read')
    })

@app.route('/api/sessions', methods=['GET'])
def get_all_sessions():
    """Get all chat sessions (admin endpoint)"""
    sessions_summary = []
    for session_id, conv in conversations.items():
        sessions_summary.append({
            'session_id': session_id,
            'created_at': conv['created_at'],
            'last_read': conv.get('last_read'),
            'message_count': len(conv['messages']),
            'last_message': conv['messages'][-1]['message'] if conv['messages'] else None,
            'has_feedback': 'feedback' in conv
        })
    
    return jsonify({
        'sessions': sessions_summary,
        'total_count': len(sessions_summary)
    })

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets (admin endpoint)"""
    return jsonify({
        'tickets': tickets,
        'total_count': len(tickets),
        'open_count': len([t for t in tickets if t['status'] == 'Open']),
        'closed_count': len([t for t in tickets if t['status'] == 'Closed'])
    })

@app.route('/api/leave-requests', methods=['GET'])
def get_leave_requests():
    """Get all leave requests (admin endpoint)"""
    return jsonify({
        'leave_requests': leave_requests,
        'total_count': len(leave_requests),
        'pending_count': len([lr for lr in leave_requests if lr['status'] == 'Pending']),
        'approved_count': len([lr for lr in leave_requests if lr['status'] == 'Approved'])
    })

@app.route('/api/employees/<employee_id>/dependents', methods=['GET'])
def get_employee_dependents(employee_id):
    """Get dependents for an employee"""
    employee_dependents = [d for d in dependents if d['employee_id'] == employee_id]
    return jsonify({
        'employee_id': employee_id,
        'dependents': employee_dependents,
        'count': len(employee_dependents)
    })

@app.route('/api/holidays', methods=['GET'])
def get_holidays():
    """Get holiday list"""
    return jsonify({
        'holidays': holidays,
        'year': 2025,
        'count': len(holidays)
    })

@app.route('/api/benefit-plans', methods=['GET'])
def get_benefit_plans():
    """Get benefit plans"""
    return jsonify({
        'benefit_plans': benefit_plans,
        'count': len(benefit_plans)
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    return jsonify({
        'total_sessions': len(conversations),
        'total_tickets': len(tickets),
        'total_leave_requests': len(leave_requests),
        'total_dependents': len(dependents),
        'open_tickets': len([t for t in tickets if t['status'] == 'Open']),
        'pending_leaves': len([lr for lr in leave_requests if lr['status'] == 'Pending']),
        'today_sessions': len([c for c in conversations.values() 
                              if c['created_at'].startswith(datetime.now().strftime('%Y-%m-%d'))]),
        'satisfaction_rate': calculate_satisfaction_rate()
    })

def calculate_satisfaction_rate():
    """Calculate satisfaction rate from feedback"""
    feedbacks = [conv.get('feedback') for conv in conversations.values() if conv.get('feedback')]
    if not feedbacks:
        return 0
    
    satisfied_count = len([f for f in feedbacks if f['type'] == 'satisfied'])
    return round((satisfied_count / len(feedbacks)) * 100, 2)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(conversations),
        'version': '1.0.0',
        'uptime': 'Running'
    })

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'HR Bot API is running',
        'version': '1.0.0',
        'endpoints': {
            'start_chat': 'POST /api/chat/start',
            'send_message': 'POST /api/chat/{session_id}/send',
            'submit_form': 'POST /api/chat/{session_id}/submit-form',
            'submit_feedback': 'POST /api/chat/{session_id}/feedback',
            'chat_history': 'GET /api/chat/{session_id}/history',
            'health_check': 'GET /api/health'
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    print("🤖 HR Bot API Starting...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📚 API Documentation at: http://localhost:5000")
    print("🏥 Health check at: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)