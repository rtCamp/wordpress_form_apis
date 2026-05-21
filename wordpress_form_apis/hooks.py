app_name = "wordpress_form_apis"
app_title = "WordPress Form APIs"
app_publisher = "rtCamp"
app_description = "Frappe APIs for WordPress form integrations (Gravity Forms, etc.)"
app_email = "support@rtcamp.com"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "wordpress_form_apis",
# 		"logo": "/assets/wordpress_form_apis/logo.png",
# 		"title": "WordPress Form APIs",
# 		"route": "/wordpress_form_apis",
# 		"has_permission": "wordpress_form_apis.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/wordpress_form_apis/css/wordpress_form_apis.css"
# app_include_js = "/assets/wordpress_form_apis/js/wordpress_form_apis.js"

# include js, css files in header of web template
# web_include_css = "/assets/wordpress_form_apis/css/wordpress_form_apis.css"
# web_include_js = "/assets/wordpress_form_apis/js/wordpress_form_apis.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "wordpress_form_apis/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "wordpress_form_apis/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "wordpress_form_apis.utils.jinja_methods",
# 	"filters": "wordpress_form_apis.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "wordpress_form_apis.install.before_install"
# after_install = "wordpress_form_apis.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "wordpress_form_apis.uninstall.before_uninstall"
# after_uninstall = "wordpress_form_apis.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "wordpress_form_apis.utils.before_app_install"
# after_app_install = "wordpress_form_apis.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "wordpress_form_apis.utils.before_app_uninstall"
# after_app_uninstall = "wordpress_form_apis.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "wordpress_form_apis.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wordpress_form_apis.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"wordpress_form_apis.tasks.all"
# 	],
# 	"daily": [
# 		"wordpress_form_apis.tasks.daily"
# 	],
# 	"hourly": [
# 		"wordpress_form_apis.tasks.hourly"
# 	],
# 	"weekly": [
# 		"wordpress_form_apis.tasks.weekly"
# 	],
# 	"monthly": [
# 		"wordpress_form_apis.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "wordpress_form_apis.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "wordpress_form_apis.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "wordpress_form_apis.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "wordpress_form_apis.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["wordpress_form_apis.utils.before_request"]
# after_request = ["wordpress_form_apis.utils.after_request"]

# Job Events
# ----------
# before_job = ["wordpress_form_apis.utils.before_job"]
# after_job = ["wordpress_form_apis.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"wordpress_form_apis.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

