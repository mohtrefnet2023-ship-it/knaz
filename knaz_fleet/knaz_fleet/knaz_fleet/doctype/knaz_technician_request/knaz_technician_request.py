import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime
from knaz_fleet.utils import ensure_positive


class KnazTechnicianRequest(Document):
    def validate(self):
        if not self.workshop_order:
            frappe.throw(_("أمر الصيانة إلزامي"))
        if self.workshop_order and not self.vehicle:
            self.vehicle = frappe.db.get_value("Knaz Workshop Order", self.workshop_order, "vehicle")
        if not self.requested_date:
            self.requested_date = now_datetime()
        ensure_positive(self.estimated_cost, "التكلفة التقديرية")
        if self.request_type == "Spare Part Request":
            if not self.item:
                frappe.throw(_("الصنف إلزامي عند طلب قطعة غيار"))
            if (self.qty or 0) <= 0:
                frappe.throw(_("الكمية يجب أن تكون أكبر من صفر"))
        if self.status == "Issued" and self.supervisor_approval != "Approved":
            frappe.throw(_("لا يمكن صرف الطلب قبل اعتماد المشرف"))
