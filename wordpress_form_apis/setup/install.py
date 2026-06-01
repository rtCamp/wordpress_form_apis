import frappe

ROLE_NAME = "Gravity Form"
BOT_USER_EMAIL = "wordpress@example.com"
WRITABLE_DOCTYPES = ("CRM Lead", "File")


def after_install():
	_ensure_role()
	for doctype in WRITABLE_DOCTYPES:
		_ensure_role_perm(doctype, ROLE_NAME)
	_ensure_bot_user()
	_ensure_self_user_permission()


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


def _ensure_role_perm(doctype, role):
	if frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": role, "permlevel": 0}):
		return
	# Clone standard DocPerm rows into Custom DocPerm first — inserting any Custom DocPerm
	# row otherwise wipes all standard perms for this doctype (see frappe.permissions.get_valid_perms).
	from frappe.permissions import setup_custom_perms

	setup_custom_perms(doctype)
	frappe.get_doc(
		{
			"doctype": "Custom DocPerm",
			"parent": doctype,
			"parenttype": "DocType",
			"parentfield": "permissions",
			"role": role,
			"permlevel": 0,
			"read": 0,
			"create": 1,
			"export": 0,
		}
	).insert(ignore_permissions=True)
	frappe.clear_cache(doctype=doctype)


def _ensure_bot_user():
	if frappe.db.exists("User", BOT_USER_EMAIL):
		return
	frappe.get_doc(
		{
			"doctype": "User",
			"email": BOT_USER_EMAIL,
			"first_name": "WordPress",
			"send_welcome_email": 0,
			"user_type": "Website User",
			"enabled": 1,
			"roles": [{"role": ROLE_NAME}],
		}
	).insert(ignore_permissions=True)


def _ensure_self_user_permission():
	"""Scope every User-link lookup the bot makes to itself.

	`apply_to_all_doctypes=1` makes Frappe filter any list/search query on a
	doctype with a User link field to records where that link equals the bot.
	Closes the User-enumeration leaks via both `frappe.client.get_list?doctype=User`
	and `frappe.desk.search.search_link?doctype=User` (the narrower
	`applicable_for=User` form only closed the first).

	Trade-off: the bot can't list CRM Leads owned by other users. That's fine —
	the WP plugin only writes new leads, never lists.
	"""
	if frappe.db.exists(
		"User Permission",
		{
			"user": BOT_USER_EMAIL,
			"allow": "User",
			"for_value": BOT_USER_EMAIL,
			"apply_to_all_doctypes": 1,
		},
	):
		return
	frappe.get_doc(
		{
			"doctype": "User Permission",
			"user": BOT_USER_EMAIL,
			"allow": "User",
			"for_value": BOT_USER_EMAIL,
			"apply_to_all_doctypes": 1,
		}
	).insert(ignore_permissions=True)
