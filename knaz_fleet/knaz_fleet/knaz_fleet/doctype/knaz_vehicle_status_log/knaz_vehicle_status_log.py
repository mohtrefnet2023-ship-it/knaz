import frappe
from frappe import _
from frappe.model.document import Document


class KnazVehicleStatusLog(Document):
    def before_save(self):
        if not self.is_new() and not frappe.has_permission("Knaz Vehicle Status Log", "write", self.name):
            frappe.throw(_("لا يمكن تعديل سجل حالة السيارة"))
