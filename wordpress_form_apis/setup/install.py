import frappe

ROLE_NAME = "Gravity Form"
USER_TYPE_NAME = "Bot User"
BOT_USER_EMAIL = "wordpress@example.com"


def after_install():
	_ensure_role()
	_ensure_user_type()
	_ensure_bot_user()


def _ensure_role():
	if frappe.db.exists("Role", ROLE_NAME):
		return
	frappe.get_doc(
		{
			"doctype": "Role",
			"role_name": ROLE_NAME,
			"desk_access": 0,
			"is_custom": 1,
		}
	).insert(ignore_permissions=True)


def _ensure_user_type():
	if frappe.db.exists("User Type", USER_TYPE_NAME):
		return
	frappe.get_doc(
		{
			"doctype": "User Type",
			"name": USER_TYPE_NAME,
			"role": ROLE_NAME,
			"is_standard": 0,
			"user_doctypes": [
				{"document_type": "CRM Lead", "read": 1, "create": 1},
			],
		}
	).insert(ignore_permissions=True)


def _ensure_bot_user():
	if frappe.db.exists("User", BOT_USER_EMAIL):
		return
	frappe.get_doc(
		{
			"doctype": "User",
			"email": BOT_USER_EMAIL,
			"first_name": "WordPress",
			"send_welcome_email": 0,
			"user_type": USER_TYPE_NAME,
			"enabled": 1,
		}
	).insert(ignore_permissions=True)
