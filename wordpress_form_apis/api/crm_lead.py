import frappe
from frappe.handler import upload_file


@frappe.whitelist(methods=["POST"])
def create():
	try:
		payload = _filter_payload(frappe.form_dict, "CRM Lead")
		attachments = payload.pop("attachments", None)
		file_ids = payload.pop("file_ids", None)

		lead = frappe.get_doc({"doctype": "CRM Lead", **payload})
		lead.save()

		# Files already uploaded via upload_lead_file: relink the unattached ones by id
		# (no duplicate). A file id that is already attached elsewhere is not moved;
		# instead its file_url is queued below to create a new File that shares the
		# same stored object. get_list scopes both to files the caller can read.
		ids = [fid.strip() for fid in (file_ids or "").split(",") if fid.strip()]
		if ids:
			rows = frappe.get_list(
				"File",
				filters={"name": ["in", ids]},
				fields=["name", "attached_to_name", "file_url"],
			)
			unattached = [r.name for r in rows if not r.attached_to_name]
			if unattached:
				frappe.db.set_value(
					"File",
					{"name": ["in", unattached]},
					{
						"attached_to_doctype": "CRM Lead",
						"attached_to_name": lead.name,
						"is_private": 1,
					},
				)
			reuse = [r.file_url for r in rows if r.attached_to_name and r.file_url]
			if reuse:
				attachments = ",".join([attachments, *reuse]) if attachments else ",".join(reuse)

		# External URLs (and reused file urls above): create new File pointers.
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
		"file_id": data.name,
		"file_name": data.get("file_name"),
		"file_url": data.get("file_url"),
	}


@frappe.whitelist(methods=["GET"])
def get_lead_sources():
	return {"lead_sources": frappe.get_all("CRM Lead Source", pluck="name", order_by="name asc")}


def _filter_payload(form_dict, doctype):
	"""Drop keys not declared on the target doctype's meta; pass through attachment keys."""
	allowed = {f.fieldname for f in frappe.get_meta(doctype).fields}
	passthrough = {"attachments", "file_ids"}
	return {k: v for k, v in form_dict.items() if k in allowed or k in passthrough}
