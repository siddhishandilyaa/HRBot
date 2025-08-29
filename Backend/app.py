from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__, template_folder="../Front end", static_folder="../Front end/static")
CORS(app)

# Enhanced user credentials with Indian employee data
USERS = {
    "admin": {"password": "password123", "role": "admin", "emp_id": "EMP001"},
    "hr": {"password": "hrpass", "role": "hr", "emp_id": "EMP002"},
    "rajesh.kumar": {"password": "rajesh123", "role": "employee", "emp_id": "EMP003"},
    "priya.sharma": {"password": "priya123", "role": "employee", "emp_id": "EMP004"},
    "amit.gupta": {"password": "amit123", "role": "manager", "emp_id": "EMP005"},
    "sneha.patel": {"password": "sneha123", "role": "employee", "emp_id": "EMP006"},
    "vikram.singh": {"password": "vikram123", "role": "employee", "emp_id": "EMP007"},
    "kavya.reddy": {"password": "kavya123", "role": "employee", "emp_id": "EMP008"},
    "arjun.nair": {"password": "arjun123", "role": "employee", "emp_id": "EMP009"},
    "ananya.joshi": {"password": "ananya123", "role": "employee", "emp_id": "EMP010"},
    "rahul.verma": {"password": "rahul123", "role": "employee", "emp_id": "EMP011"},
    "pooja.agarwal": {"password": "pooja123", "role": "manager", "emp_id": "EMP012"},
    "karthik.menon": {"password": "karthik123", "role": "employee", "emp_id": "EMP013"},
    "deepika.iyer": {"password": "deepika123", "role": "employee", "emp_id": "EMP014"},
    "rohit.malhotra": {"password": "rohit123", "role": "employee", "emp_id": "EMP015"}
}

# Mock employee database with Indian names
EMPLOYEE_DATA = {
    "EMP001": {
        "name": "Suresh Raina", "department": "Administration", "position": "Administrator",
        "manager": "CEO", "hire_date": "2020-01-01", "salary": 120000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+91-98765-43201"
    },
    "EMP002": {
        "name": "Meera Krishnan", "department": "Human Resources", "position": "HR Manager",
        "manager": "CEO", "hire_date": "2020-02-01", "salary": 100000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+91-98765-43202"
    },
    "EMP003": {
        "name": "Rajesh Kumar", "department": "Engineering", "position": "Software Developer",
        "manager": "Amit Gupta", "hire_date": "2022-03-15", "salary": 75000,
        "leave_balance": {"annual": 18, "sick": 8}, "phone": "+91-98765-43203"
    },
    "EMP004": {
        "name": "Priya Sharma", "department": "Marketing", "position": "Marketing Specialist",
        "manager": "Pooja Agarwal", "hire_date": "2021-07-20", "salary": 65000,
        "leave_balance": {"annual": 15, "sick": 6}, "phone": "+91-98765-43204"
    },
    "EMP005": {
        "name": "Amit Gupta", "department": "Engineering", "position": "Engineering Manager",
        "manager": "Suresh Raina", "hire_date": "2020-01-10", "salary": 95000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+91-98765-43205"
    },
    "EMP006": {
        "name": "Sneha Patel", "department": "Finance", "position": "Financial Analyst",
        "manager": "Pooja Agarwal", "hire_date": "2023-01-08", "salary": 70000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+91-98765-43206"
    },
    "EMP007": {
        "name": "Vikram Singh", "department": "Engineering", "position": "Senior Developer",
        "manager": "Amit Gupta", "hire_date": "2019-11-12", "salary": 85000,
        "leave_balance": {"annual": 12, "sick": 4}, "phone": "+91-98765-43207"
    },
    "EMP008": {
        "name": "Kavya Reddy", "department": "HR", "position": "HR Coordinator",
        "manager": "Meera Krishnan", "hire_date": "2022-09-05", "salary": 55000,
        "leave_balance": {"annual": 16, "sick": 7}, "phone": "+91-98765-43208"
    },
    "EMP009": {
        "name": "Arjun Nair", "department": "Sales", "position": "Sales Representative",
        "manager": "Pooja Agarwal", "hire_date": "2023-06-01", "salary": 60000,
        "leave_balance": {"annual": 20, "sick": 9}, "phone": "+91-98765-43209"
    },
    "EMP010": {
        "name": "Ananya Joshi", "department": "Design", "position": "UX Designer",
        "manager": "Amit Gupta", "hire_date": "2021-12-03", "salary": 72000,
        "leave_balance": {"annual": 14, "sick": 5}, "phone": "+91-98765-43210"
    },
    "EMP011": {
        "name": "Rahul Verma", "department": "Operations", "position": "Operations Specialist",
        "manager": "Pooja Agarwal", "hire_date": "2020-08-17", "salary": 58000,
        "leave_balance": {"annual": 19, "sick": 8}, "phone": "+91-98765-43211"
    },
    "EMP012": {
        "name": "Pooja Agarwal", "department": "Management", "position": "Department Manager",
        "manager": "Suresh Raina", "hire_date": "2018-04-22", "salary": 90000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+91-98765-43212"
    },
    "EMP013": {
        "name": "Karthik Menon", "department": "IT", "position": "System Administrator",
        "manager": "Amit Gupta", "hire_date": "2022-11-30", "salary": 68000,
        "leave_balance": {"annual": 17, "sick": 6}, "phone": "+91-98765-43213"
    },
    "EMP014": {
        "name": "Deepika Iyer", "department": "Legal", "position": "Legal Assistant",
        "manager": "Pooja Agarwal", "hire_date": "2023-02-14", "salary": 52000,
        "leave_balance": {"annual": 21, "sick": 10}, "phone": "+91-98765-43214"
    },
    "EMP015": {
        "name": "Rohit Malhotra", "department": "Customer Support", "position": "Support Specialist",
        "manager": "Amit Gupta", "hire_date": "2022-05-10", "salary": 48000,
        "leave_balance": {"annual": 20, "sick": 8}, "phone": "+91-98765-43215"
    }
}

def get_employee_info(username):
    """Get employee information by username"""
    if username not in USERS:
        return None
    
    emp_id = USERS[username]["emp_id"]
    if emp_id not in EMPLOYEE_DATA:
        return None
    
    return EMPLOYEE_DATA[emp_id]

# In-memory chat history store (per user)
CHAT_HISTORY = {}
# In-memory leave application state per user
LEAVE_STATE = {}
# In-memory leave requests for HR approval
LEAVE_REQUESTS = []

# In-memory support tickets
SUPPORT_TICKETS = []
TICKET_CATEGORIES = ["Payroll Issue", "Technical", "ID Card", "Policy Issue", "Other"]

# Add a mock assignment and updates/comments for demonstration
def get_ticket_assigned_to(ticket):
    # Assign to HR or IT Support based on category
    cat = ticket["category"].lower()
    if "payroll" in cat or "policy" in cat:
        return "HR Team"
    elif "technical" in cat or "id card" in cat:
        return "IT Support"
    else:
        return "Support Team"

def get_ticket_updates(ticket):
    # For demo, show a static update if status is not Open
    if ticket["status"] == "Open":
        return "No updates yet."
    elif ticket["status"] == "In Progress":
        return "Your ticket is being reviewed by our team."
    elif ticket["status"] == "Resolved":
        return "Your issue has been resolved."
    elif ticket["status"] == "Closed":
        return "Ticket closed. Please contact support if you have further issues."
    else:
        return "No updates yet."

def get_holiday_list():
    holidays = "\n".join([f"{h['name']}: {h['date']}" for h in HOLIDAYS])
    return f"🎉 **Upcoming Holidays:**\n{holidays}"

def find_hr_response(message, username):
    """Find the most appropriate HR response based on keywords and user role"""
    message_lower = message.lower()
    emp_info = get_employee_info(username)
    user_role = USERS[username]["role"]

    # General conversational replies
    if any(word in message_lower for word in ["thank you", "thanks", "thx", "thankyou"]):
        return "You're welcome! 😊 If you need anything else, just ask."
    if any(word in message_lower for word in ["bye", "goodbye", "see you", "see ya", "see u"]):
        return "Goodbye! Have a great day! 👋"
    if any(word in message_lower for word in ["how are you", "how r u", "how are u", "how's it going"]):
        return "I'm good, How can I assist you today?"
    if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! How can I help you today?"

    # Feedback form link (only show after leave flow, not here)
    if any(word in message_lower for word in ["feedback", "feedback form"]):
        return (
            '<a href="https://docs.google.com/forms/d/e/1FAIpQLSf5FqAAR8MZa36yiTM_YfEJ_HObnHdexKrfV0fyBOxwg4Wkkg/viewform?usp=header" target="_blank">'
            '📝 Open Employee Feedback Form</a>'
        )

    # Show holiday list if asked
    if any(word in message_lower for word in ["holiday list", "holidays", "public holidays", "festival"]):
        return get_holiday_list()

    # --- Leave Application Flow for Employees/Managers ---
    if user_role in ["employee", "manager"]:
        state = LEAVE_STATE.get(username, {})

        # Allow user to cancel leave application at any step
        if message_lower in ["stop", "cancel", "exit", "quit"]:
            if username in LEAVE_STATE:
                LEAVE_STATE.pop(username, None)
                return "🚫 Leave application process cancelled."
            # If not in flow, just ignore
            # ...continue to other responses...

        # Step 1: Initiate leave application
        if ("apply leave" in message_lower or "leave application" in message_lower) and not state:
            LEAVE_STATE[username] = {"step": 1}
            return (
                "📝 **Want to apply for leave?**\n"
                "When do you want to apply for leave? (Leave start date)\n"
                "Please provide the date in this format: DD-MM-YY\n"
                "Type `stop` or `cancel` to exit leave application at any time."
            )
        # Step 2: Get start date
        if state.get("step") == 1:
            # Try to parse date in DD-MM-YY
            try:
                start_date = datetime.strptime(message.strip(), "%d-%m-%y")
                LEAVE_STATE[username] = {"step": 2, "start_date": start_date.strftime("%d-%m-%Y")}
                # Updated leave types with Indian context
                leave_types = [
                    "Vacation Leave",
                    "Sick Leave",
                    "COVID-19 Related Absence",
                    "Bereavement Leave",
                    "Comp/In Lieu Time",
                    "FMLA"
                ]
                leave_list = "\n".join([f"{i+1}. {lt}" for i, lt in enumerate(leave_types)])
                # Get employee leave balance with total and remaining
                leave_balance = ""
                if emp_info and "leave_balance" in emp_info:
                    total_annual = 21  # Assuming company policy
                    total_sick = 10    # Assuming company policy
                    remaining_annual = emp_info['leave_balance'].get('annual', 0)
                    remaining_sick = emp_info['leave_balance'].get('sick', 0)
                    leave_balance = (
                        f"Your Leave Balance:\n"
                        f"• Total Annual: {total_annual} days | Remaining: {remaining_annual} days\n"
                        f"• Total Sick: {total_sick} days | Remaining: {remaining_sick} days\n"
                    )
                return (
                    "Please wait while I grab your available leaves data.\n"
                    "It takes a few seconds.\n\n"
                    f"{leave_balance}"
                    "Here are your available leaves:\n"
                    f"{leave_list}\n\n"
                    "What is the reason for your leave? (Please select one of the above or type your reason)\n"
                    "Type `stop` or `cancel` to exit leave application at any time."
                )
            except Exception:
                return "❌ Please provide the date in the correct format: DD-MM-YY"
        # Step 3: Get leave reason
        if state.get("step") == 2:
            LEAVE_STATE[username] = {
                "step": 3,
                "start_date": state["start_date"],
                "reason": message.strip()
            }
            return (
                "When is the end date of leave?\n"
                "Please provide the date in this format: DD-MM-YY\n"
                "Type `/stop` or `cancel` to exit leave application at any time."
            )
        # Step 4: Get end date and finish
        if state.get("step") == 3:
            try:
                end_date = datetime.strptime(message.strip(), "%d-%m-%y")
                start_date = state["start_date"]
                reason = state["reason"]
                LEAVE_STATE.pop(username, None)
                # Store leave request for HR approval
                LEAVE_REQUESTS.append({
                    "employee": emp_info["name"] if emp_info else username,
                    "emp_id": USERS[username]["emp_id"],
                    "start_date": start_date,
                    "end_date": end_date.strftime('%d-%m-%Y'),
                    "reason": reason,
                    "status": "Pending"
                })
                # Remove feedback links from the response
                return (
                    f"✅ Your leave application has been recorded.\n"
                    f"Start Date: {start_date}\n"
                    f"End Date: {end_date.strftime('%d-%m-%Y')}\n"
                    f"Reason: {reason}\n"
                    "Your request will be sent to your manager for approval.\n\n"
                    "Thank you for using the leave application service!\n"
                )
            except Exception:
                return "❌ Please provide the end date in the correct format: DD-MM-YY"
    # --- End Leave Application Flow ---

    # --- HR Leave Management ---
    if user_role == "hr":
        # Remove apply leave for HR, replace with leave requests option
        if "apply leave" in message_lower or "leave application" in message_lower:
            return (
                "🗂️ As HR, you can view and manage employee leave requests.\n"
                "• To see all employee leave balances, type: `employee leaves`\n"
                "• To see pending leave requests, type: `leave requests`\n"
                "• To approve/dismiss, type: `approve <number>` or `dismiss <number>`"
            )

        # Show all employee leave balances
        if any(word in message_lower for word in ["employee leaves", "show leaves", "all leaves", "leave balance"]):
            response = "🗂️ **Employee Leave Balances:**\n\n"
            for emp_id, emp in EMPLOYEE_DATA.items():
                response += (
                    f"• {emp['name']} (ID: {emp_id}) - "
                    f"Annual: {emp['leave_balance'].get('annual', 0)} days, "
                    f"Sick: {emp['leave_balance'].get('sick', 0)} days\n"
                )
            return response

        # Show pending leave requests for approval
        if any(word in message_lower for word in ["leave requests", "pending leaves", "approve leave", "leave approvals"]):
            if not LEAVE_REQUESTS or all(r["status"] != "Pending" for r in LEAVE_REQUESTS):
                return "📋 There are no pending leave requests at the moment."
            response = "📋 **Pending Leave Requests:**\n\n"
            for idx, req in enumerate(LEAVE_REQUESTS):
                if req["status"] == "Pending":
                    response += (
                        f"Request #{idx+1}:\n"
                        f"• Employee: {req['employee']} (ID: {req['emp_id']})\n"
                        f"• Start Date: {req['start_date']}\n"
                        f"• End Date: {req['end_date']}\n"
                        f"• Reason: {req['reason']}\n"
                        f"• Status: {req['status']}\n"
                        f"To approve: type `approve {idx+1}`\n"
                        f"To dismiss: type `dismiss {idx+1}`\n\n"
                    )
            return response

        # Approve or dismiss a leave request
        if message_lower.startswith("approve ") or message_lower.startswith("dismiss "):
            parts = message_lower.split()
            if len(parts) == 2 and parts[1].isdigit():
                req_idx = int(parts[1]) - 1
                if 0 <= req_idx < len(LEAVE_REQUESTS):
                    req = LEAVE_REQUESTS[req_idx]
                    if req["status"] != "Pending":
                        return f"Request #{req_idx+1} has already been processed."
                    if message_lower.startswith("approve "):
                        req["status"] = "Approved"
                        action_msg = (
                            f"✅ Leave request for {req['employee']} (ID: {req['emp_id']}) "
                            f"from {req['start_date']} to {req['end_date']} has been **APPROVED**.\n"
                        )
                    else:
                        req["status"] = "Dismissed"
                        action_msg = (
                            f"❌ Leave request for {req['employee']} (ID: {req['emp_id']}) "
                            f"from {req['start_date']} to {req['end_date']} has been **DISMISSED**.\n"
                        )
                    # Show remaining pending requests, if any
                    remaining = [r for r in LEAVE_REQUESTS if r["status"] == "Pending"]
                    if remaining:
                        response = "📋 **Remaining Pending Leave Requests:**\n\n"
                        for idx, r in enumerate(LEAVE_REQUESTS):
                            if r["status"] == "Pending":
                                response += (
                                    f"Request #{idx+1}:\n"
                                    f"• Employee: {r['employee']} (ID: {r['emp_id']})\n"
                                    f"• Start Date: {r['start_date']}\n"
                                    f"• End Date: {r['end_date']}\n"
                                    f"• Reason: {r['reason']}\n"
                                    f"• Status: {r['status']}\n"
                                    f"To approve: type `approve {idx+1}`\n"
                                    f"To dismiss: type `dismiss {idx+1}`\n\n"
                                )
                        return action_msg + response
                    else:
                        return action_msg + "📋 There are no pending leave requests at the moment."
                else:
                    return "Invalid request number."
            else:
                return "Invalid command format. Use `approve <number>` or `dismiss <number>`."

    # Admin users - Technical queries only
    if user_role == "admin":
        if any(word in message_lower for word in ["server", "system", "database", "backup", "maintenance", "technical", "logs", "performance"]):
            return "🔧 **Technical System Information:**\n\n" \
                   "• **System Status:** All services running normally\n" \
                   "• **Database:** Connected and optimized\n" \
                   "• **Last Backup:** " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n" \
                   "• **Server Uptime:** 99.9%\n" \
                   "• **Performance:** Optimal\n\n" \
                   "🛠️ **Available Actions:**\n" \
                   "• System monitoring\n• Database maintenance\n• Backup management\n• Performance optimization"
        
        if any(word in message_lower for word in ["users", "accounts", "reset password", "access", "permissions"]):
            return "👥 **User Management:**\n\n" \
                   f"• **Total Users:** {len(USERS)}\n" \
                   f"• **Active Employees:** {len(EMPLOYEE_DATA)}\n" \
                   "• **Recent Logins:** Available in system logs\n\n" \
                   "🔐 **Admin Functions:**\n" \
                   "• Reset user passwords\n• Manage user access\n• View system logs\n• Configure permissions"
        
        return "🔧 **Admin Technical Support**\n\nI can help you with:\n" \
               "• 🖥️ System status and monitoring\n• 🗄️ Database management\n• 👥 User account management\n" \
               "• 🔒 Security and permissions\n• 📊 System performance\n• 🛠️ Technical maintenance\n\n" \
               "What technical assistance do you need?"
    
    # HR users - Full access to all employee data
    elif user_role == "hr":
        # Employee lookup queries
        if any(word in message_lower for word in ["employee", "staff", "worker", "find", "search", "lookup"]):
            # Extract potential employee name from message
            employee_found = None
            for emp_id, emp_data in EMPLOYEE_DATA.items():
                emp_name_parts = emp_data['name'].lower().split()
                if any(part in message_lower for part in emp_name_parts):
                    employee_found = emp_data
                    break
            
            if employee_found:
                return f"👤 **Employee Details:**\n\n" \
                       f"**Name:** {employee_found['name']}\n" \
                       f"**Department:** {employee_found['department']}\n" \
                       f"**Position:** {employee_found['position']}\n" \
                       f"**Manager:** {employee_found['manager']}\n" \
                       f"**Hire Date:** {employee_found['hire_date']}\n" \
                       f"**Salary:** ₹{employee_found['salary']:,}\n" \
                       f"**Contact:** {employee_found['phone']}\n" \
                       f"**Leave Balance:** Annual: {employee_found['leave_balance']['annual']} | Sick: {employee_found['leave_balance']['sick']}"
            else:
                # Show all employees list
                response = "👥 **All Employees:**\n\n"
                for emp_id, emp_data in EMPLOYEE_DATA.items():
                    response += f"• **{emp_data['name']}** - {emp_data['department']} - {emp_data['position']}\n"
                return response
        
        # Department wise employee list
        if any(word in message_lower for word in ["department", "team", "division"]):
            dept_employees = {}
            for emp_id, emp_data in EMPLOYEE_DATA.items():
                dept = emp_data['department']
                if dept not in dept_employees:
                    dept_employees[dept] = []
                dept_employees[dept].append(emp_data['name'])
            
            response = "🏢 **Department-wise Employee List:**\n\n"
            for dept, employees in dept_employees.items():
                response += f"**{dept}:**\n"
                for emp in employees:
                    response += f"  • {emp}\n"
                response += "\n"
            return response
        
        # Salary information for all employees
        if any(word in message_lower for word in ["salary", "payroll", "compensation", "pay"]):
            response = "💰 **Salary Information (All Employees):**\n\n"
            total_payroll = 0
            for emp_id, emp_data in EMPLOYEE_DATA.items():
                response += f"• **{emp_data['name']}:** ₹{emp_data['salary']:,}/year\n"
                total_payroll += emp_data['salary']
            response += f"\n**Total Company Payroll:** ₹{total_payroll:,}/year"
            return response
        
        # Attendance for all employees
        if any(word in message_lower for word in ["attendance", "present", "absent", "late"]):
            return "📊 **Attendance Overview:**\n\n" \
                   "• **Total Employees:** " + str(len(EMPLOYEE_DATA)) + "\n" \
                   "• **Present Today:** " + str(random.randint(85, 95)) + "%\n" \
                   "• **On Leave:** " + str(random.randint(3, 8)) + " employees\n" \
                   "• **Late Arrivals:** " + str(random.randint(1, 5)) + " employees\n\n" \
                   "📈 **Monthly Attendance Trend:**\n" \
                   "• Week 1: 92%\n• Week 2: 89%\n• Week 3: 94%\n• Week 4: 91%"
        
        # Default HR response
        return "👥 **HR Management Dashboard**\n\nI can help you with:\n" \
               "• 👤 Employee information and lookup\n• 🏢 Department-wise reports\n• 💰 Salary and payroll data\n" \
               "• 📊 Attendance tracking\n• 📋 Leave management\n• 📈 Performance reports\n\n" \
               "What would you like to know about?"
    
    # Regular employees and managers
    else:
        # Personal information queries
        if any(word in message_lower for word in ["my", "me", "myself", "personal", "profile"]):
            if emp_info:
                return f"👤 **Your Profile:**\n\n" \
                       f"**Name:** {emp_info['name']}\n" \
                       f"**Employee ID:** {USERS[username]['emp_id']}\n" \
                       f"**Department:** {emp_info['department']}\n" \
                       f"**Position:** {emp_info['position']}\n" \
                       f"**Manager:** {emp_info['manager']}\n" \
                       f"**Hire Date:** {emp_info['hire_date']}\n" \
                       f"**Contact:** {emp_info['phone']}\n" \
                       f"**Leave Balance:** Annual: {emp_info['leave_balance']['annual']} | Sick: {emp_info['leave_balance']['sick']}"
            else:
                return "❌ Sorry, I couldn't find your employee information. Please contact HR."
        
        # Salary queries
        if any(word in message_lower for word in ["salary", "pay", "payroll", "compensation"]):
            # If in ticket creation flow and selected Payroll Issue, prompt for issue details instead of showing salary info
            state = LEAVE_STATE.get(username, {})
            if state.get("ticket_step") == 1 and (
                state.get("ticket_category", "").lower() == "payroll issue" or
                message_lower.strip() == "payroll issue"
            ):
                LEAVE_STATE[username] = {"ticket_step": 2, "ticket_category": "Payroll Issue"}
                return "Please describe your issue in detail."
            if emp_info:
                return f"💰 **Your Salary Information:**\n\n" \
                       f"**Basic Salary:** ₹{emp_info['salary']:,}/year\n" \
                       f"**Monthly:** ₹{emp_info['salary']//12:,}\n" \
                       f"**Pay Date:** 28th of every month\n" \
                       f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}\n\n" \
                       f"💳 **Benefits:**\n" \
                       f"• Health Insurance\n• Provident Fund\n• Gratuity\n• Performance Bonus"
            else:
                return "❌ Sorry, I couldn't find your salary information. Please contact HR."
        
        # Leave queries
        if any(word in message_lower for word in ["leave", "vacation", "time off", "holiday"]):
            if emp_info:
                # Leave balances
                leave_info = (
                    f"🏖️ **Your Leave Information:**\n\n"
                    f"**Annual Leave Balance:** {emp_info['leave_balance']['annual']} days\n"
                    f"**Sick Leave Balance:** {emp_info['leave_balance']['sick']} days\n"
                    f"**Total Available:** {emp_info['leave_balance']['annual'] + emp_info['leave_balance']['sick']} days\n\n"
                    f"📋 **Leave Policy:**\n"
                    f"• Annual Leave: 21 days/year\n"
                    f"• Sick Leave: 10 days/year\n"
                    f"• Personal Leave: 5 days/year\n"
                    f"• Maternity Leave: 26 weeks\n\n"
                    f"📝 **To Apply Leave:**\n"
                    f"Contact your manager: {emp_info['manager']}\n"
                )
                # Show leave request status for this user
                emp_id = USERS[username]["emp_id"]
                user_requests = [r for r in LEAVE_REQUESTS if r["emp_id"] == emp_id]
                if user_requests:
                    status_vocab = {
                        "Pending": "**Pending**",
                        "Approved": "**Approved**",
                        "Dismissed": "**Rejected**"
                    }
                    leave_info += "\n🗂️ **Your Leave Requests Status:**\n"
                    for idx, req in enumerate(user_requests, 1):
                        status_word = status_vocab.get(req["status"], f"**{req['status']}**")
                        leave_info += (
                            f"{idx}. {req['start_date']} to {req['end_date']} | Reason: {req['reason']} | "
                            f"Status: {status_word}\n"
                        )
                return leave_info
            else:
                return "❌ Sorry, I couldn't find your leave information. Please contact HR."
        
        # Attendance queries
        if any(word in message_lower for word in ["attendance", "present", "absent", "late", "check in"]):
            return "📊 **Your Attendance:**\n\n" \
                   "**Today's Status:** Present ✅\n" \
                   "**Check-in Time:** 9:15 AM\n" \
                   "**This Month:** 18/20 days present\n" \
                   "**Attendance Rate:** 90%\n\n" \
                   "📈 **Recent Attendance:**\n" \
                   "• Monday: Present\n• Tuesday: Present\n• Wednesday: Present\n• Thursday: Present\n• Friday: Present"
        
        # Benefits queries
        if any(word in message_lower for word in ["benefit", "insurance", "medical", "health"]):
            return "🏥 **Your Benefits:**\n\n" \
                   "**Health Insurance:**\n" \
                   "• Coverage: Self + Family\n" \
                   "• Network: All major hospitals\n" \
                   "• Annual Limit: ₹5,00,000\n\n" \
                   "**Other Benefits:**\n" \
                   "• Life Insurance: 3x annual salary\n" \
                   "• Provident Fund: 12% + 12%\n" \
                   "• Gratuity: As per law\n" \
                   "• Performance Bonus: Up to 20%\n\n" \
                   "📞 **For Claims:** Contact HR at ext. 1234"
        
        # Policy queries
        if any(word in message_lower for word in ["policy issue", "rule", "guideline", "procedure"]):
            # If in ticket creation flow, treat as ticket category selection
            state = LEAVE_STATE.get(username, {})
            if state.get("ticket_step") == 1:
                LEAVE_STATE[username] = {"ticket_step": 2, "ticket_category": "Policy Issue"}
                return (
                    "You selected **Policy Issue**.\n"
                    "Please describe your issue in detail."
                )
            # Otherwise, show company policies as usual
            return "📋 **Company Policies:**\n\n" \
                   "**Work Hours:** 9:00 AM - 6:00 PM\n" \
                   "**Dress Code:** Business Casual\n" \
                   "**Remote Work:** 2 days/week allowed\n" \
                   "**Overtime:** Pre-approved required\n" \
                   "**Expense Policy:** Submit within 30 days\n\n" \
                   "📖 **Full Policy Manual:** Available on company portal"
        
        # General help
        if any(word in message_lower for word in ["help", "assist", "support"]):
            return "🤖 **How can I help you?**\n\n" \
                   "I can assist with:\n" \
                   "• 👤 Your personal information\n" \
                   "• 💰 Salary details\n" \
                   "• 🏖️ Leave balance and applications\n" \
                   "• 📊 Attendance tracking\n" \
                   "• 🏥 Benefits and insurance\n" \
                   "• 📋 Company policies\n" \
                   "• 📞 Contact information\n\n" \
                   "Just ask me anything!"

        # --- Support Ticket Creation Flow ---
        # Create ticket flow - Step 1: Start ticket creation
        if "create ticket" in message_lower and "ticket_category" not in LEAVE_STATE.get(username, {}):
            LEAVE_STATE[username] = {"ticket_step": 1}
            categories = "\n".join([f"{i+1}. {cat}" for i, cat in enumerate(TICKET_CATEGORIES)])
            return (
                "Please select a category for your issue:\n"
                f"{categories}\n"
                "Type the category name or number."
            )

        # Create ticket flow - Step 2: Select category
        state = LEAVE_STATE.get(username, {})
        if state.get("ticket_step") == 1:
            selected = message.strip().lower()
            category = None
            # Match by number or name
            if selected.isdigit() and 1 <= int(selected) <= len(TICKET_CATEGORIES):
                category = TICKET_CATEGORIES[int(selected)-1]
            else:
                for cat in TICKET_CATEGORIES:
                    if cat.lower() in selected:
                        category = cat
                        break
            if category:
                LEAVE_STATE[username] = {"ticket_step": 2, "ticket_category": category}
                return "Please describe your issue in detail."
            else:
                return "Invalid category. Please type the category name or number from the list."

        # Create ticket flow - Step 3: Enter issue description
        if state.get("ticket_step") == 2 and "ticket_category" in state:
            issue_desc = message.strip()
            ticket_no = f"TKT{len(SUPPORT_TICKETS)+1:04d}"
            ticket_category = state["ticket_category"]
            assigned_to = get_ticket_assigned_to({"category": ticket_category})
            SUPPORT_TICKETS.append({
                "ticket_no": ticket_no,
                "username": username,
                "category": ticket_category,
                "description": issue_desc,
                "status": "Open",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "assigned_to": assigned_to,
                "updates": "No updates yet."
            })
            LEAVE_STATE.pop(username, None)
            return (
                f"Your ticket has been created.\n"
                f"Ticket No: **{ticket_no}**\n"
                f"Assigned To: {assigned_to}\n"
                "Thank you! We'll get back to you soon."
            )

        # Show ticket details for user
        if "get ticket details" in message_lower or "my tickets" in message_lower:
            user_tickets = [t for t in SUPPORT_TICKETS if t["username"] == username]
            if not user_tickets:
                return "You have no support tickets."
            response = "🎫 **Your Support Tickets:**\n"
            for t in user_tickets:
                response += (
                    f"• **Ticket No:** {t['ticket_no']}\n"
                    f"  **Issue:** {t['description']}\n"
                    f"  **Created Date:** {t['created_at']}\n"
                    f"  **Current Status:** {t['status']}\n"
                    f"  **Assigned To:** {t.get('assigned_to', get_ticket_assigned_to(t))}\n"
                    f"  **Updates/Comments:** {t.get('updates', get_ticket_updates(t))}\n\n"
                )
            return response

    # HR: View all support tickets and take action
    if USERS[username]["role"] == "hr":
        # Accept both "All tickets" and "All Tickets" (case-insensitive)
        if "support tickets" in message_lower or "all tickets" in message_lower:
            if not SUPPORT_TICKETS:
                return "There are no support tickets at the moment."
            response = "🎫 **All Support Tickets:**\n"
            for idx, t in enumerate(SUPPORT_TICKETS, 1):
                response += (
                    f"{idx}. **Ticket No:** {t['ticket_no']}\n"
                    f"   **User:** {t['username']}\n"
                    f"   **Category:** {t['category']}\n"
                    f"   **Issue:** {t['description']}\n"
                    f"   **Created Date:** {t['created_at']}\n"
                    f"   **Current Status:** {t['status']}\n"
                    f"   **Assigned To:** {t.get('assigned_to', get_ticket_assigned_to(t))}\n"
                    f"   **Updates/Comments:** {t.get('updates', get_ticket_updates(t))}\n"
                    f"   To approve: type `approve ticket {idx}`\n"
                    f"   To close: type `close ticket {idx}`\n\n"
                )
            return response

        # HR: Approve or close a support ticket
        if message.lower().startswith("approve ticket ") or message.lower().startswith("close ticket "):
            parts = message.lower().split()
            if len(parts) == 3 and parts[2].isdigit():
                idx = int(parts[2]) - 1
                if 0 <= idx < len(SUPPORT_TICKETS):
                    ticket = SUPPORT_TICKETS[idx]
                    if message.lower().startswith("approve ticket "):
                        ticket["status"] = "Resolved"
                        ticket["updates"] = "Ticket approved and resolved by HR."
                        return f"Ticket {ticket['ticket_no']} has been approved and marked as resolved."
                    else:
                        # Prompt for comments/feedback before closing
                        LEAVE_STATE[username] = {"close_ticket_idx": idx}
                        return (
                            f"Please provide comments/feedback for closing Ticket {ticket['ticket_no']}.\n"
                            "Type your comments below."
                        )
                else:
                    return "Invalid ticket number."
            else:
                return "Invalid command. Use `approve ticket <number>` or `close ticket <number>`."

        # Handle HR feedback/comments for closing ticket
        state = LEAVE_STATE.get(username, {})
        if "close_ticket_idx" in state:
            idx = state["close_ticket_idx"]
            if 0 <= idx < len(SUPPORT_TICKETS):
                ticket = SUPPORT_TICKETS[idx]
                ticket["status"] = "Closed"
                ticket["updates"] = f"Ticket closed by HR. Comments: {message.strip()}"
                LEAVE_STATE.pop(username, None)
                return f"Ticket {ticket['ticket_no']} has been closed with your comments."
            else:
                LEAVE_STATE.pop(username, None)
                return "Invalid ticket reference for closing."

    # Default response for unrecognized input
    return "🤖 **HR Assistant**\n\n" \
           "I can help you with:\n" \
           "• 👤 Your personal information\n" \
           "• 💰 Salary details\n" \
           "• 🏖️ Leave balance and applications\n" \
           "• 📊 Attendance tracking\n" \
           "• 🏥 Benefits information\n" \
           "• 📋 Company policies\n\n" \
           "What would you like to know about?"

def generate_attendance_data(emp_id, days=30):
    """Generate mock attendance data for an employee"""
    attendance_data = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        # Skip weekends
        if date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            continue
            
        # Generate random attendance data
        status = random.choice(['Present', 'Present', 'Present', 'Present', 'Present', 'Present', 'Present', 'Present', 'Present', 'Absent'])
        check_in = None
        check_out = None
        
        if status == 'Present':
            # Random check-in time between 8:30 AM and 10:00 AM
            check_in_hour = random.randint(8, 9)
            check_in_minute = random.randint(0, 59) if check_in_hour == 8 else random.randint(0, 30)
            check_in = f"{check_in_hour:02d}:{check_in_minute:02d}"
            
            # Random check-out time between 5:30 PM and 7:00 PM
            check_out_hour = random.randint(17, 18)
            check_out_minute = random.randint(0, 59)
            check_out = f"{check_out_hour:02d}:{check_out_minute:02d}"
        
        attendance_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'status': status,
            'check_in': check_in,
            'check_out': check_out
        })
    
    return attendance_data

# In-memory chat history store (per user)
CHAT_HISTORY = {}
# In-memory leave application state per user
LEAVE_STATE = {}

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle user login with simple welcome messages"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid request format."}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required."}), 400
        
        if username in USERS and USERS[username]["password"] == password:
            # Clear previous chat history on login
            CHAT_HISTORY.pop(username, None)
            emp_info = get_employee_info(username)
            user_role = USERS[username]["role"]
            
            # Simple welcome messages based on role
            if user_role == "admin":
                if emp_info:
                    first_name = emp_info['name'].split()[0]
                    welcome_msg = f"Hello {first_name}, Welcome back !!"
                else:
                    welcome_msg = "Hello Admin, Welcome back !!"
            elif user_role == "hr":
                if emp_info:
                    first_name = emp_info['name'].split()[0]
                    welcome_msg = f"Hello {first_name}, Welcome back !!"
                else:
                    welcome_msg = "Hello HR, Welcome back !!"
            else:
                # For regular employees
                if emp_info:
                    first_name = emp_info['name'].split()[0]
                    welcome_msg = f"Hello {first_name}, Welcome back !!"
                else:
                    welcome_msg = f"Hello {username}, Welcome back !!"
            
            return jsonify({
                "success": True,
                "message": welcome_msg,
                "username": username,
                "role": user_role
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
        
        # Store chat history (if needed)
        CHAT_HISTORY.setdefault(username, []).append({
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        return jsonify({
            "success": True,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": timestamp
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Debug logging
        return jsonify({
            "success": False,
            "message": "Server error during chat. Please try again."
        }), 500

@app.route('/employee/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    """Get employee information by employee ID"""
    try:
        if emp_id not in EMPLOYEE_DATA:
            return jsonify({
                "success": False,
                "message": "Employee not found."
            }), 404
            
        return jsonify({
            "success": True,
            "employee": EMPLOYEE_DATA[emp_id]
        })
        
    except Exception as e:
        print(f"Employee lookup error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Server error during employee lookup."
        }), 500

@app.route('/attendance/<username>', methods=['GET'])
def get_attendance(username):
    """Get attendance data for a user"""
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

@app.route('/logout', methods=['POST'])
def logout():
    """Clear user session (dummy logout)"""
    try:
        data = request.get_json()
        username = data.get("username", "")
        # You can also clear session/cookies here if using Flask-Login

        # Clear previous chat history for the user
        CHAT_HISTORY.pop(username, None)

        return jsonify({
            "success": True,
            "message": f"User {username} has been logged out successfully."
        })
    except Exception as e:
        return jsonify({"success": False, "message": "Logout failed."}), 500

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
    
    sample_users = ["rajesh.kumar", "priya.sharma", "amit.gupta", "admin", "hr"]
    for user in sample_users:
        if user in USERS:
            emp_info = get_employee_info(user)
            name = emp_info["name"] if emp_info else "N/A"
            role = USERS[user]["role"]
            print(f"   👤 {user:<15} | {USERS[user]['password']:<10} | {role:<8} | {name}")
    
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