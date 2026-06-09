import frappe
from frappe.utils import today, add_days, getdate
from knaz_fleet.utils import days_overdue, create_notification_for_role


def update_overdue_collections():
    if not frappe.db.table_exists("Knaz Collection Case"):
        return
    for name in frappe.get_all("Knaz Collection Case", filters={"status": ["not in", ["Collected", "Closed"]]}, pluck="name"):
        doc = frappe.get_doc("Knaz Collection Case", name)
        doc.delay_days = days_overdue(doc.due_date)
        if doc.status == "Promise to Pay" and doc.promise_date and getdate(doc.promise_date) < getdate(today()) and (doc.outstanding_amount or 0) > 0:
            doc.status = "Promise Broken"
        doc.save(ignore_permissions=True)


def update_overdue_finance_installments():
    if not frappe.db.table_exists("Knaz Finance Installment"):
        return
    for name in frappe.get_all("Knaz Finance Installment", filters={"status": ["in", ["Upcoming", "Due", "Partially Paid"]]}, pluck="name"):
        doc = frappe.get_doc("Knaz Finance Installment", name)
        if doc.due_date and getdate(doc.due_date) < getdate(today()) and (doc.outstanding_amount or 0) > 0:
            doc.status = "Overdue"
            doc.save(ignore_permissions=True)


def create_document_expiry_alerts():
    if frappe.db.table_exists("Knaz Vehicle"):
        target = add_days(today(), 30)
        for v in frappe.get_all("Knaz Vehicle", filters={"insurance_expiry_date": ["between", [today(), target]]}, fields=["name", "plate_no", "insurance_expiry_date"]):
            create_notification_for_role(f"تأمين السيارة {v.plate_no} سينتهي بتاريخ {v.insurance_expiry_date}", "Knaz Vehicle", v.name, "Knaz Operations Manager")
    if frappe.db.table_exists("Knaz Legal Session"):
        target = add_days(today(), 3)
        for s in frappe.get_all("Knaz Legal Session", filters={"session_date": ["between", [today(), target]]}, fields=["name", "legal_case", "session_date"]):
            create_notification_for_role(f"جلسة قضية قادمة بتاريخ {s.session_date}", "Knaz Legal Session", s.name, "Knaz Legal Officer")
