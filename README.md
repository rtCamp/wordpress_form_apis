# WordPress Form APIs

Frappe-side endpoints for the Gravity Forms → Frappe CRM integration.

The companion WordPress plugin lives at **[rtCamp/gravityforms-frappecrm](https://github.com/rtCamp/gravityforms-frappecrm)** — install it on the WordPress site that hosts the forms, point its API base URL at this Frappe site, and use the bot user's API token (see Setup below).

## What it ships

| Endpoint | Purpose |
|---|---|
| `wordpress_form_apis.api.doctype.get_doctype_list` | Returns the list of CRM doctypes that can be targeted (currently `CRM Lead`). Used by the WP plugin to populate its **Document Type** dropdown. |
| `wordpress_form_apis.api.doctype.get_doctype_fields` | Returns the fields of a given doctype (standard + custom). Used by the WP plugin to populate its **Field Values** mapping. |
| `wordpress_form_apis.api.crm_lead.create` | Creates a `CRM Lead` from POST data. Only keys present in `CRM Lead`'s meta (incl. custom fields) are accepted; the synthetic `attachments` key is parsed as a comma-separated list of file URLs. |
| `wordpress_form_apis.api.crm_lead.upload_lead_file` | Uploads a private file and returns its URL — to be passed back as part of `attachments` on the `create` call. |
| `wordpress_form_apis.api.crm_lead.get_lead_sources` | Returns the list of `CRM Lead Source` names — to populate a source dropdown when mapping the `source` field. |

All endpoints require an authenticated request (no `allow_guest`). The plugin signs requests with the bot user's Frappe API token.

## Requirements

- Frappe v16+
- [Frappe CRM](https://github.com/frappe/crm) installed on the same site (declared as `required_apps`).

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/rtCamp/wordpress_form_apis --branch develop
bench --site <your-site> install-app wordpress_form_apis
```

The `after_install` hook will automatically:

1. Create a custom role named **`Gravity Form`** (`is_custom=1`, `desk_access=0`).
2. Add Custom DocPerm entries on `CRM Lead` and `File` granting the role `Create` only (every other flag, including `read` and `export`, explicitly `0`).
3. Create a bot user **`wordpress@example.com`** as `user_type = Website User` with the `Gravity Form` role, no welcome email, no password. (Frappe auto-sets the user type to `Website User` when no assigned role has `desk_access`; the install hook just declares the same explicitly.)
4. Add a `User Permission` for the bot scoped `Allow = User, For Value = wordpress@example.com, Apply To All Document Types = 1`. Any list/search query against a doctype that has a `User` link field is constrained to records where the link value equals the bot — closes Frappe's baseline user-enumeration leak across both `frappe.client.get_list` and `frappe.desk.search.search_link`.

All three steps are idempotent — re-running install (or `bench migrate` followed by a re-install) skips anything that already exists.

## Setup

### 1. Generate the bot user's API key & secret

1. Open `/app/user/wordpress@example.com` on your Frappe site.
2. Click **Settings (the gear icon) → API Access**.
3. Click **Generate Keys**. A toast will show the **API Secret** — **copy it now**; Frappe will not show it again. Also copy the **API Key** from the same panel.
4. The token to use in the WordPress plugin is:

   ```
   <api_key>:<api_secret>
   ```

   And the full `Authorization` header value is:

   ```
   token <api_key>:<api_secret>
   ```

### 2. Customize the bot user (optional)

If you want to rename `wordpress@example.com` to something tied to your domain (`wordpress@<your-domain>` etc.), edit the User record after install. The role + permissions stay attached.

The bot user is a `Website User` whose only role is `Gravity Form` (`desk_access=0`). The role's Custom DocPerm grants `create` on `CRM Lead` and `File` only (`read=0, write=0, export=0`); nothing else is writable. A `User Permission` constrains the bot to see only itself across any User-link lookup. The bot has no password — the only way it authenticates is via its API token.

### 3. Configure the WordPress plugin

Install **[rtCamp/gravityforms-frappecrm](https://github.com/rtCamp/gravityforms-frappecrm)** on your WordPress site, then in **GravityForms → Settings → ERPNext Connect**:

| Field | Value |
|---|---|
| API Key | `token <api_key>:<api_secret>` (with the literal word `token` and a space) |
| API Base URL | `https://<your-frappe-site>/api/method/` |

Then for each Gravity Form, **Form Settings → ERPNext Connect → Create Feed**:

| Field | Value |
|---|---|
| Request URL | `https://<your-frappe-site>/api/method/wordpress_form_apis.api.crm_lead.create` |
| Request Method | `POST` |
| Request Format | `JSON` |
| Document Type | `CRM Lead` (the dropdown is populated from this app's discovery endpoint) |
| Field Values | Map your form fields to `CRM Lead` fields. Anything not present on the doctype's meta will be silently dropped server-side. |

For attachments, the plugin should upload the file first via `…/api/method/wordpress_form_apis.api.crm_lead.upload_lead_file`, then pass the returned URL(s) as a comma-separated value under the `attachments` key in the `create` body.

## Field allowlist (security note)

`create` accepts any field declared on `CRM Lead`'s meta — standard fields and any `custom_*` fields installed on the site. The role permission gate is `Create` only on `CRM Lead`; any further policy on which fields a form may write must be enforced either in the WP plugin's field-mapping UI or via a `CRM Lead` server script (`before_insert` / `validate`) on the Frappe side.

## License

agpl-3.0
