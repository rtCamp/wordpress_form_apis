# WordPress Form APIs

Frappe-side endpoints for the Gravity Forms → Frappe CRM integration.

The companion WordPress plugin lives at **[rtCamp/gravityforms-erpnextcrm](https://github.com/rtCamp/gravityforms-erpnextcrm)** — install it on the WordPress site that hosts the forms, point its API base URL at this Frappe site, and use the bot user's API token (see Setup below).

## What it ships

| Endpoint | Purpose |
|---|---|
| `wordpress_form_apis.api.doctype.get_doctype_list` | Returns the list of CRM doctypes that can be targeted (currently `CRM Lead`). Used by the WP plugin to populate its **Document Type** dropdown. |
| `wordpress_form_apis.api.doctype.get_doctype_fields` | Returns the fields of a given doctype (standard + custom). Used by the WP plugin to populate its **Field Values** mapping. |
| `wordpress_form_apis.api.crm_lead.create` | Creates a `CRM Lead` from POST data. Only keys present in `CRM Lead`'s meta (incl. custom fields) are accepted; the synthetic `attachments` key is parsed as a comma-separated list of file URLs. |
| `wordpress_form_apis.api.crm_lead.upload_lead_file` | Uploads a private file and returns its URL — to be passed back as part of `attachments` on the `create` call. |

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
2. Create a non-standard User Type named **`Bot User`** that:
   - Binds the `Gravity Form` role.
   - Grants `Read` + `Create` on `CRM Lead`.
   - Frappe auto-adds `Read` + `Create` + `Write` on `File` for every non-standard User Type.
   - Blocks every module not used by the declared doctypes — the user cannot reach the rest of the desk even if they log in.
3. Create a bot user **`wordpress@example.com`** with `user_type = Bot User`, no welcome email, no password. The User Type assignment sets the role automatically.

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

The bot user is created with `user_type = Bot User` (a non-standard User Type shipped by this app). It can call whitelisted methods on `CRM Lead` and `File` only; every other module is in `block_modules` so the desk surface is effectively closed even if someone forces a login.

### 3. Configure the WordPress plugin

Install **[gravityforms-erpnextcrm](https://github.com/rtCamp/gravityforms-erpnextcrm)** on your WordPress site, then in **GravityForms → Settings → ERPNext Connect**:

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
