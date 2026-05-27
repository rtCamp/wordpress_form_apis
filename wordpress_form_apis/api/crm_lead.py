import frappe
from frappe.handler import upload_file


@frappe.whitelist(methods=["POST"])
def create():
	try:
		payload = _filter_payload(frappe.form_dict, "CRM Lead")
		attachments = payload.pop("attachments", None)

		lead = frappe.get_doc({"doctype": "CRM Lead", **payload})
		lead.save()

		if attachments:
			for attachment_url in attachments.split(","):
				attachment_url = attachment_url.strip()
				if not attachment_url:
					continue
				frappe.get_doc(
					{
						"doctype": "File",
						"attached_to_doctype": "CRM Lead",
						"attached_to_name": lead.name,
						"is_private": 1,
						"file_url": attachment_url,
					}
				).insert()
		return {
			"status": "success",
			"message": "Lead created successfully",
			"lead_name": lead.name,
		}
	except Exception as e:
		frappe.log_error(title="Lead Creation Failed", message=str(e))
		return {
			"status": "error",
			"message": str(e),
		}


@frappe.whitelist(methods=["POST"])
def upload_lead_file():
	frappe.form_dict.is_private = 1
	data = upload_file()
	return {
		"file_name": data.get("file_name"),
		"file_url": data.get("file_url"),
	}


@frappe.whitelist(methods=["GET"])
def get_lead_sources():
	return {"lead_sources": frappe.get_all("CRM Lead Source", pluck="name", order_by="name asc")}


def _filter_payload(form_dict, doctype):
	"""Drop keys not declared on the target doctype's meta; pass through 'attachments'."""
	allowed = {f.fieldname for f in frappe.get_meta(doctype).fields}
	return {k: v for k, v in form_dict.items() if k in allowed or k == "attachments"}
