app_name = "wordpress_form_apis"
app_title = "WordPress Form APIs"
app_publisher = "rtCamp"
app_description = "Frappe APIs for WordPress form integrations (Gravity Forms, etc.)"
app_email = "frappe@rtcamp.com"
app_license = "agpl-3.0"

required_apps = ["crm"]

after_install = "wordpress_form_apis.setup.install.after_install"
