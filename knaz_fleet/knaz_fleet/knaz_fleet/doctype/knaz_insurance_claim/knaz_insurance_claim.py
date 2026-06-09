import frappe
from frappe import _
from frappe.model.document import Document
from knaz_fleet.utils import ensure_positive


class KnazInsuranceClaim(Document):
    def validate(self):
        for fieldname, label in [
            ("estimated_amount", "مبلغ التقدير"),
            ("claim_amount", "مبلغ المطالبة"),
            ("approved_amount", "مبلغ التعويض المعتمد"),
            ("received_amount", "مبلغ التعويض المستلم"),
        ]:
            ensure_positive(self.get(fieldname), label)
        if float(self.received_amount or 0) > float(self.approved_amount or 0) and float(self.approved_amount or 0) > 0:
            if not frappe.has_permission("Knaz Insurance Claim", "submit"):
                frappe.throw(_("التعويض المستلم لا يجب أن يتجاوز المعتمد"))
        if self.status == "Closed" and self.status == "Missing Documents":
            frappe.throw(_("لا يمكن إغلاق مطالبة ناقصة المستندات"))
