import frappe
from frappe import _


@frappe.whitelist()
def create_workshop_order_from_accident(accident):
    acc = frappe.get_doc("Knaz Vehicle Accident", accident)
    doc = frappe.new_doc("Knaz Workshop Order")
    doc.vehicle = acc.vehicle
    doc.maintenance_type = "Accident Repair"
    doc.issue_description = acc.accident_description
    doc.accident = acc.name
    doc.entry_date = frappe.utils.now_datetime()
    doc.insert()
    acc.db_set("workshop_order", doc.name)
    acc.db_set("status", "Under Repair")
    return doc.name


@frappe.whitelist()
def create_insurance_claim_from_accident(accident, insurance_company=None):
    acc = frappe.get_doc("Knaz Vehicle Accident", accident)
    doc = frappe.new_doc("Knaz Insurance Claim")
    doc.accident = acc.name
    doc.vehicle = acc.vehicle
    doc.insurance_company = insurance_company or frappe.db.get_value("Knaz Vehicle", acc.vehicle, "insurance_company")
    if not doc.insurance_company:
        frappe.throw(_("شركة التأمين مطلوبة لإنشاء المطالبة"))
    doc.claim_date = frappe.utils.today()
    doc.insert()
    acc.db_set("insurance_claim", doc.name)
    acc.db_set("status", "Insurance Claim Opened")
    frappe.db.set_value("Knaz Vehicle", acc.vehicle, "current_status", "Insurance Claim")
    return doc.name
