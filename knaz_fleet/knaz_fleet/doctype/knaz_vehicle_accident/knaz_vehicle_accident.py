import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today


class KnazVehicleAccident(Document):
    def validate(self):
        if getdate(self.accident_date) > getdate(today()):
            frappe.throw(_("تاريخ الحادث لا يجب أن يكون في المستقبل"))
        if self.fault_percentage is not None and not (0 <= float(self.fault_percentage or 0) <= 100):
            frappe.throw(_("نسبة الخطأ يجب أن تكون بين 0 و 100"))

    def after_insert(self):
        frappe.db.set_value("Knaz Vehicle", self.vehicle, "current_status", "Accident")
