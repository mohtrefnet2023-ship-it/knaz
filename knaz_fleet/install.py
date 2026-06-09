import frappe
from frappe import _

ROLES = [
    "Knaz General Manager",
    "Knaz Operations Manager",
    "Knaz Accountant",
    "Knaz Collection Officer",
    "Knaz Workshop Supervisor",
    "Knaz Technician",
    "Knaz Store Keeper",
    "Knaz Insurance Officer",
    "Knaz Legal Officer",
]


def after_install():
    create_roles()
    create_default_alert_rules()
    create_workspace()


def create_roles():
    for role in ROLES:
        if not frappe.db.exists("Role", role):
            doc = frappe.new_doc("Role")
            doc.role_name = role
            doc.desk_access = 1
            doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_alert_rules():
    if not frappe.db.table_exists("Knaz System Alert Rule"):
        return
    defaults = [
        ("Vehicle Insurance Expiry", 30, "Knaz Operations Manager", "تنبيه: تأمين السيارة سينتهي قريبًا"),
        ("Vehicle Registration Expiry", 30, "Knaz Operations Manager", "تنبيه: استمارة السيارة ستنتهي قريبًا"),
        ("Finance Installment Due", 7, "Knaz Accountant", "تنبيه: قسط تمويل مستحق قريبًا"),
        ("Legal Session Due", 3, "Knaz Legal Officer", "تنبيه: جلسة قضية قادمة"),
    ]
    for alert_type, days_before, role, template in defaults:
        if not frappe.db.exists("Knaz System Alert Rule", {"alert_type": alert_type, "target_role": role}):
            doc = frappe.new_doc("Knaz System Alert Rule")
            doc.alert_type = alert_type
            doc.days_before = days_before
            doc.target_role = role
            doc.message_template = template
            doc.active = 1
            doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_workspace():
    # Workspace schema can vary across Frappe versions, so keep this intentionally defensive.
    if not frappe.db.exists("DocType", "Workspace"):
        return
    name = "Knaz Fleet Operations"
    if frappe.db.exists("Workspace", name):
        return
    try:
        workspace = frappe.new_doc("Workspace")
        workspace.label = name
        workspace.title = name
        workspace.module = "Knaz Fleet"
        workspace.public = 1
        workspace.is_hidden = 0
        workspace.content = "[]"
        workspace.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Knaz Fleet workspace creation skipped")
