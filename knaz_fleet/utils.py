import frappe
from frappe import _
from frappe.utils import getdate, today


def ensure_positive(value, label):
    if value is not None and float(value or 0) < 0:
        frappe.throw(_("{0} لا يمكن أن يكون قيمة سالبة").format(_(label)))


def ensure_gt_zero(value, label):
    if float(value or 0) <= 0:
        frappe.throw(_("{0} يجب أن يكون أكبر من صفر").format(_(label)))


def validate_date_order(start_date, end_date, message=None):
    if start_date and end_date and getdate(end_date) <= getdate(start_date):
        frappe.throw(_(message or "تاريخ النهاية يجب أن يكون بعد تاريخ البداية"))


def create_notification_for_role(subject, document_type=None, document_name=None, role=None):
    """Create Notification Log entries for users who have a role. Fails softly for cloud safety."""
    if not role or not frappe.db.exists("Role", role):
        return
    users = frappe.get_all("Has Role", filters={"role": role, "parenttype": "User"}, pluck="parent")
    for user in users:
        if user in ("Administrator", "Guest"):
            continue
        try:
            log = frappe.new_doc("Notification Log")
            log.subject = subject
            log.for_user = user
            log.type = "Alert"
            log.document_type = document_type
            log.document_name = document_name
            log.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Knaz notification creation failed")


def days_overdue(date_value):
    if not date_value:
        return 0
    return max((getdate(today()) - getdate(date_value)).days, 0)
