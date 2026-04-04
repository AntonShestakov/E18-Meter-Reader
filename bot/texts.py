"""
User-facing strings for E18 Meter Reader Bot.

All button labels, messages, prompts, and responses are defined here.
This centralizes text management and simplifies i18n preparation.
"""

# Welcome & Start Messages
START_MESSAGE = """
Welcome to the E18 Meter Reading Bot! 👋

This bot helps you submit and track meter readings for your apartment building.

What would you like to do?
"""

HELP_MESSAGE = """
📖 **Help**

This bot helps you manage meter readings for your building.

**Your role determines what you can do:**
- **Tenant**: Submit readings for your apartment
- **Grayhound**: Submit readings for any apartment in the building
- **Administrator**: Manage users, assign roles, monitor all readings

Use the buttons below to navigate.
"""

NEW_USER_MESSAGE = """
Hello! 👋 You're a new user.

Before you can submit meter readings, you need to request access. An administrator will review your request and assign you an appropriate role.

Would you like to request access?
"""

# Button Labels
BUTTON_SUBMIT_READING = "📊 Submit Reading"
BUTTON_VIEW_READINGS = "📈 View Readings / Chart"
BUTTON_VIEW_OWN_READINGS = "📈 View Own Readings / Chart"
BUTTON_EXPORT_CSV = "📥 Export Readings (CSV)"
BUTTON_REQUEST_SUBMEETING = "📋 Request for Meter Submeeting"
BUTTON_ASSIGN_ROLES = "👥 Assign / Revoke Roles"
BUTTON_MANAGE_USERS = "➕ Add / Deactivate Users"
BUTTON_MANAGE_APARTMENTS = "🏠 Manage Apartment List"
BUTTON_REQUESTS = "📬 Requests"
BUTTON_ABOUT = "ℹ️ About Bot"

# Numeric Pad
BUTTON_0 = "0️⃣"
BUTTON_1 = "1️⃣"
BUTTON_2 = "2️⃣"
BUTTON_3 = "3️⃣"
BUTTON_4 = "4️⃣"
BUTTON_5 = "5️⃣"
BUTTON_6 = "6️⃣"
BUTTON_7 = "7️⃣"
BUTTON_8 = "8️⃣"
BUTTON_9 = "9️⃣"
BUTTON_CLEAR = "🔄 Clear"
BUTTON_SUBMIT = "✅ Submit"
BUTTON_CANCEL = "❌ Cancel"

# Navigation
BUTTON_BACK = "← Back"
BUTTON_CONFIRM = "✔️ Confirm"
BUTTON_DENY = "✘ Deny"

# Reading Submission
READING_PROMPT = "💡 Enter meter reading (numeric input only)"
READING_SUBMITTED = "✅ Reading submitted! Current value: {value} kWh"
READING_ERROR = "❌ Error: {error}\n\nPlease try again."
INVALID_READING = "❌ Invalid reading. Please enter a number."
READING_TOO_LOW = "⚠️ Warning: Reading seems unusually low ({value} kWh). Continue?"
READING_TOO_HIGH = "⚠️ Warning: Reading seems unusually high ({value} kWh). Continue?"

# Role Management
ASSIGN_ROLE_PROMPT = "👥 Select a user to assign a role:"
REVOKE_ROLE_PROMPT = "👥 Select a user to revoke a role:"
ROLE_ASSIGNED = "✅ Role assigned: {user} is now a {role}"
ROLE_REVOKED = "✅ Role revoked: {user} no longer has {role}"
INVALID_ROLE = "❌ Invalid role selected."

# Apartment Management
SELECT_APARTMENT = "🏢 Select an apartment:"
ADD_APARTMENT_PROMPT = "📝 Enter apartment number:"
APARTMENT_ADDED = "✅ Apartment {number} added (Floor {floor})"
APARTMENT_DELETED = "✅ Apartment {number} deleted"
INVALID_APARTMENT = "❌ Apartment not found."

# Errors & Warnings
PERMISSION_DENIED = "🚫 You don't have permission to perform this action."
DATABASE_ERROR = "❌ Database error. Please try again later."
INVALID_INPUT = "❌ Invalid input. Please try again."
SESSION_EXPIRED = "⏰ Your session has expired. Use /start to begin again."
UNEXPECTED_ERROR = "😞 Something went wrong. Please try again later."

# About
ABOUT_BOT = """
📱 **E18 Meter Reading Bot**

Version: 1.0.0
Purpose: Streamline meter reading submissions for residential buildings

**Features:**
- Submit meter readings quickly
- Track reading history
- Export readings to CSV
- Role-based access control

Questions? Contact your building administrator.
"""
